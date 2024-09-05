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
    waiting_for_edit_or_finish = State()


def make_user_options_menu():
    return make_row_keyboard_by_list([
        'Редактировать имя',
        'Завершить',
    ])


@router.message(lambda message: message.text == 'Добавить пользователя')
async def add_user(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddUserState.waiting_for_name)


@router.message(AddUserState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    old_name = (await state.get_data()).get('name')
    await state.update_data(name=name)
    if old_name:
        await message.answer(f"Вы изменили имя с {old_name} на {name}")
    else:
        await message.answer(f"Имя пользователя установлено: {name}")

    await message.answer("Выберите действие:", reply_markup=make_user_options_menu())
    await state.set_state(AddUserState.waiting_for_edit_or_finish)


@router.message(AddUserState.waiting_for_edit_or_finish)
async def process_user_option(message: types.Message, state: FSMContext):
    button_text = message.text
    name = (await state.get_data()).get('name')

    if button_text == 'Редактировать имя':
        await message.answer("Введите новое имя пользователя:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddUserState.waiting_for_name)
    elif button_text == 'Завершить':
        await message.answer(f"Вы добавили пользователя по имени {name}")
        await message.answer("Выберите действие:", reply_markup=make_main_menu())
        await state.clear()
