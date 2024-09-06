import json

import requests
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from decouple import config

from src.bot.common import contact_fields, BASE_URL, print_contact_by_name
from src.bot.handlers.main import make_main_menu
from src.bot.keyboards.simple_row_by_list import make_row_keyboard_by_list

router = Router()


class EditContactState(StatesGroup):
    waiting_for_name = State()
    waiting_for_choosing_what_to_edit = State()
    waiting_for_data = State()


def make_edit_user_menu():
    return make_row_keyboard_by_list([
        *[w.capitalize() for w in contact_fields],
        'Finish',
    ])


@router.message(StateFilter(None), F.text == 'Edit contact')
async def get_contact_name(message: types.Message, state: FSMContext):
    await message.answer("Type contact name:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(EditContactState.waiting_for_name)


@router.message(EditContactState.waiting_for_name)
async def edit_contact(message: types.Message, state: FSMContext):
    name = message.text
    res = requests.get(f'{BASE_URL}/contacts/name/{name}')
    res_json = res.json()
    await state.update_data(name=name)
    await state.update_data(id=res_json.get('id'))
    await state.set_state(EditContactState.waiting_for_choosing_what_to_edit)
    await message.answer(f'Find contact {name} with data:\n' + print_contact_by_name(name))
    await message.answer('Choose what to edit', reply_markup=make_edit_user_menu())


@router.message(EditContactState.waiting_for_choosing_what_to_edit)
async def edit_contact(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get('name')
    button_text = message.text

    if button_text == 'Finish':
        await message.answer(
            f'Now {name} has this data:\n' + print_contact_by_name(name),
            reply_markup=make_main_menu()
        )
        await state.clear()
        return

    if button_text.lower() in contact_fields:
        await message.answer(
            f'Type new {button_text.lower()}:',
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(field_to_update=button_text.lower())
        await state.set_state(EditContactState.waiting_for_data)
        return

    await message.answer("Error. Choose menu option.", reply_markup=make_edit_user_menu())

@router.message(EditContactState.waiting_for_data)
async def update_field_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    field_to_update: str = user_data.get('field_to_update')

    if field_to_update:
        id = user_data.get('id')
        contact = requests.put(f'{BASE_URL}/contacts/{id}', data=json.dumps({field_to_update: message.text})).json()
        print(contact)
        await message.answer(
            f"{field_to_update.capitalize()} changed to {contact[field_to_update]}.",
            reply_markup=make_edit_user_menu()
        )
        await state.set_state(EditContactState.waiting_for_choosing_what_to_edit)
        return

    await message.answer("Error", reply_markup=make_edit_user_menu())
