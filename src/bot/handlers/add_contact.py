import json
from typing import Dict

import requests
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from decouple import config

from src.bot.common import print_contact_by_name
# from src.bot.handlers.edit_contact import make_edit_user_menu, EditContactState
from src.bot.handlers.main import make_main_menu
from src.bot.keyboards.simple_row_by_list import make_row_keyboard_by_list

router = Router()

BASE_URL = 'http://0.0.0.0:8000'


class AddContactState(StatesGroup):
    waiting_for_name = State()
    # waiting_for_choosing_edit_or_finish = State()
    # waiting_for_edit = State()
    # waiting_new_field_value = State()


# def make_edit_or_finish_user_menu():
#     return make_row_keyboard_by_list([
#         'Edit user',
#         'Finish',
#     ])


@router.message(StateFilter(None), F.text == 'Add contact')
async def get_contact_name(message: types.Message, state: FSMContext):
    await message.answer("Type contact name:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddContactState.waiting_for_name)


@router.message(AddContactState.waiting_for_name)
async def add_contact(message: types.Message, state: FSMContext):
    name = message.text
    res = requests.post(BASE_URL + '/contacts', data=json.dumps({"name": name}))
    res_json = res.json()
    await message.answer(f"User {res_json['name']} added")
    await message.answer(print_contact_by_name(name), reply_markup=make_main_menu())
    await state.clear()

# @router.message(AddContactState.waiting_for_choosing_edit_or_finish)
# async def process_contact_option(message: types.Message, state: FSMContext):
#     button_text = message.text
#
#     if button_text == 'Edit contact':
#         await message.answer(
#             "Choose option:",
#             reply_markup=make_edit_user_menu()
#         )
#         await state.set_state(EditContactState.choosing_what_to_edit)
#         return
#
#     if button_text == 'Finish':
#         id = (await state.get_data()).get('id')
#         contact: Dict[str, str] = requests.get(BASE_URL + f'/contacts/{id}').json()
#         user_info_message = "\n".join([
#             f"{field.capitalize()}: {value}" for field, value in contact.items() if value != 'null'
#         ])
#         await message.answer(
#             f"Contact:\n{user_info_message}",
#             reply_markup=make_main_menu()
#         )
#         await state.clear()
#         return
