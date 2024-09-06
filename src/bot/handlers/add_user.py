import json

import requests
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from decouple import config

from src.bot.handlers.main import make_main_menu
from src.bot.keyboards.simple_row_by_list import make_row_keyboard_by_list

router = Router()

BASE_URL = 'http://0.0.0.0:8000'


class AddUserState(StatesGroup):
    waiting_for_name = State()
    waiting_for_choosing_edit_or_finish = State()
    waiting_for_edit = State()
    waiting_new_field_value = State()


# class UserFieldEnum(Enum):
#     name = 'Имя'
#     telegram = 'Telegram'
#     phone = 'Телефон'
#     birthday = 'Дата рождения'


from_button_text_to_database_fields = {
    'Имя': 'name',
    'Telegram': 'telegram',
    'Телефон': 'phone',
    'Дата рождения': 'birthday',
}


# user_fields = [
#     ('name', 'Имя'),
#     ('telegram', 'Telegram'),
#     ('phone', 'Телефон'),
#     ('birthday', 'Дата рождения'),
# ]


def make_edit_or_finish_user_menu():
    return make_row_keyboard_by_list([
        'Редактировать пользователя',
        'Завершить',
    ])


def make_edit_user_menu():
    return make_row_keyboard_by_list([
        *from_button_text_to_database_fields.keys(),
        'Отменить',
    ])


@router.message(lambda message: message.text == 'Добавить пользователя')
async def add_user(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddUserState.waiting_for_name)


@router.message(AddUserState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    input_name = message.text
    res_post = requests.post(
        BASE_URL + '/contacts',
        data=json.dumps({"name": input_name})
    )
    id = res_post.json()["id"]
    await state.update_data(id=id)
    res_get = requests.get(BASE_URL + f'/contacts/{id}')
    name = res_get.json()['name']
    await message.answer(
        f"Добавлен пользователь: {name}",
        reply_markup=make_edit_or_finish_user_menu()
    )
    await state.set_state(AddUserState.waiting_for_choosing_edit_or_finish)


@router.message(AddUserState.waiting_for_choosing_edit_or_finish)
async def process_user_option(message: types.Message, state: FSMContext):
    button_text = message.text
    user_data = await state.get_data()

    if button_text == 'Редактировать пользователя':
        await message.answer(
            "Выберите, что вы хотите редактировать:",
            reply_markup=make_edit_user_menu()
        )
        await state.set_state(AddUserState.waiting_for_edit)
        return

    if button_text == 'Завершить':
        # Формируем сообщение с данными пользователя
        # fields = from_button_text_to_database_fields.keys()
        # user_info = {field: user_data.get(field, 'Не указано') for field in fields}
        # user_info_message = "\n".join([f"{field.capitalize()}: {value}" for field, value in user_info.items()])
        id = (await state.get_data()).get('id')
        contact = requests.get(BASE_URL + f'/contacts/{id}').json()
        user_info_message = "\n".join([
            f"{field}: {value}" for field, value in contact.items()
        ])
        await message.answer(
            f"Вы добавили пользователя:\n{user_info_message}",
            reply_markup=make_main_menu()
        )
        await state.clear()
        return


@router.message(AddUserState.waiting_for_edit)
async def edit_user(message: types.Message, state: FSMContext):
    button_text = message.text

    if button_text == 'Отменить':
        await message.answer("Редактирование отменено.", reply_markup=make_edit_or_finish_user_menu())
        await state.set_state(AddUserState.waiting_for_choosing_edit_or_finish)
        return

    if button_text in from_button_text_to_database_fields.keys():
        await message.answer(
            f'Введите новый "{button_text}":',
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(current_field=from_button_text_to_database_fields[button_text])
        await state.set_state(AddUserState.waiting_new_field_value)
        return

    await message.answer("Неверный выбор. Пожалуйста, выберите опцию из меню.", reply_markup=make_edit_user_menu())


@router.message(AddUserState.waiting_new_field_value)
async def update_field_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    current_field = user_data.get('current_field')
    id = user_data.get('id')

    if current_field:
        contact = requests.put(BASE_URL + f'/contacts/{id}', data=json.dumps({current_field: message.text})).json()
        try:
            await message.answer(
                f"{current_field} обновлен на {contact[current_field]}.",
                reply_markup=make_edit_or_finish_user_menu()
            )
        except KeyError:
            print(contact)
        await state.set_state(AddUserState.waiting_for_choosing_edit_or_finish)
        return

    await message.answer("Произошла ошибка. Пожалуйста, попробуйте снова.", reply_markup=make_edit_user_menu())
