from enum import Enum

from aiogram import Router
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from decouple import config

from src.bot.handlers.main import make_main_menu
from src.bot.keyboards.simple_row_by_list import make_row_keyboard_by_list

router = Router()


class AddUserState(StatesGroup):
    waiting_for_name = State()
    waiting_for_choosing_edit_or_finish = State()
    waiting_for_choosing_what_to_edit = State()
    waiting_for_edit = State()

class UserFieldEnum(Enum):
    name = 'Имя'
    telegram = 'Telegram'
    phone = 'Телефон'
    name = 'Имя'
    name = 'Имя'
    name = 'Имя'


def make_edit_or_finish_user_menu():
    return make_row_keyboard_by_list([
        'Редактировать пользователя',
        'Завершить',
    ])


def make_edit_user_menu():
    return make_row_keyboard_by_list([
        'Имя',
        'Telegram',
        'Телефон',
        'Email',
        'Дату рождения',
        'Отменить',
    ])


@router.message(lambda message: message.text == 'Добавить пользователя')
async def add_user(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddUserState.waiting_for_name)


@router.message(AddUserState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(f"Добавлен пользователь: {name}", reply_markup=make_edit_or_finish_user_menu())
    await state.set_state(AddUserState.waiting_for_choosing_edit_or_finish)


@router.message(AddUserState.waiting_for_choosing_edit_or_finish)
async def process_user_option(message: types.Message, state: FSMContext):
    button_text = message.text
    user_data = await state.get_data()
    name = user_data.get('name')

    if button_text == 'Редактировать пользователя':
        await message.answer("Выберите, что вы хотите редактировать:", reply_markup=make_edit_user_menu())
        await state.set_state(AddUserState.waiting_for_choosing_what_to_edit)
        return

    if button_text == 'Завершить':
        # Формируем сообщение с данными пользователя
        fields = ['name', 'telegram', 'phone', 'email', 'birthdate']
        user_info = {field: user_data.get(field, 'Не указано') for field in fields}
        user_info_message = "\n".join([f"{field.capitalize()}: {value}" for field, value in user_info.items()])
        await message.answer(f"Вы добавили пользователя:\n{user_info_message}", reply_markup=make_main_menu())
        await state.clear()
        return


@router.message(AddUserState.waiting_for_choosing_what_to_edit)
async def edit_user(message: types.Message, state: FSMContext):
    field = message.text

    if field == 'Отменить':
        await message.answer("Редактирование отменено.", reply_markup=make_edit_or_finish_user_menu())
        await state.set_state(AddUserState.waiting_for_choosing_edit_or_finish)
        return

    if field in ['Имя', 'Telegram', 'Телефон', 'Email', 'Дату рождения']:
        await message.answer(f"Введите новый {field.lower()}:", reply_markup=ReplyKeyboardRemove())
        await state.update_data(current_field=field.lower())
        await state.set_state(AddUserState.waiting_for_edit)
        return

    await message.answer("Неверный выбор. Пожалуйста, выберите опцию из меню.", reply_markup=make_edit_user_menu())


@router.message(AddUserState.waiting_for_edit)
async def update_field_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    current_field = user_data.get('current_field')

    if current_field:
        await state.update_data(**{current_field: message.text})
        await message.answer(f"{current_field.capitalize()} обновлен на {message.text}.",
                             reply_markup=make_edit_or_finish_user_menu())
        await state.set_state(AddUserState.waiting_for_choosing_edit_or_finish)
        return

    await message.answer("Произошла ошибка. Пожалуйста, попробуйте снова.", reply_markup=make_edit_user_menu())
