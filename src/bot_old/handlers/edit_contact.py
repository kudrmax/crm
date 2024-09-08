# import json
#
# import requests
# from aiogram import types, Router, F
# from aiogram.filters import StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import ReplyKeyboardRemove
#
# from src.bot.common import contact_fields, BASE_URL, print_contact_by_name
# from src.bot_old.handlers.main import make_main_menu
# from src.bot_old.keyboards.simple_row_by_list import make_row_keyboard_by_list
#
# router = Router()
#
# class EditContactState(StatesGroup):
#     waiting_for_typing_name = State()
#     waiting_for_choosing_name = State()
#     waiting_for_choosing_what_to_edit = State()
#     waiting_for_data = State()
#
#
# def make_edit_user_menu():
#     return make_row_keyboard_by_list([
#         *[w.capitalize() for w in contact_fields],
#         'Finish',
#     ])
#
#
# @router.message(StateFilter(None), F.text == 'Edit contact')
# async def get_contact_name(message: types.Message, state: FSMContext):
#     await message.answer("Type contact name:", reply_markup=ReplyKeyboardRemove())
#     await state.set_state(EditContactState.waiting_for_typing_name)
#
#
# @router.message(EditContactState.waiting_for_typing_name)
# async def edit_contact(message: types.Message, state: FSMContext):
#     name = message.text
#     contacts = (requests.get(f'{BASE_URL}/contacts/search/{name}')).json()
#     contact_names = [contact['name'] for contact in contacts]
#     await message.answer(
#         'Choose contact',
#         reply_markup=make_row_keyboard_by_list(contact_names)
#     )
#     await state.set_state(EditContactState.waiting_for_choosing_name)
#
#
# @router.message(EditContactState.waiting_for_choosing_name)
# async def edit_contact(message: types.Message, state: FSMContext):
#     name = message.text
#     contact = requests.get(f'{BASE_URL}/contacts/name/{name}')
#     await state.update_data(name=name)
#     await state.update_data(id=contact.json().get('id'))
#     await message.answer(
#         f'You are editing {name}:\n' + print_contact_by_name(name),
#         reply_markup=make_edit_user_menu()
#     )
#     await state.set_state(EditContactState.waiting_for_choosing_what_to_edit)
#
#
#
# @router.message(EditContactState.waiting_for_choosing_what_to_edit)
# async def edit_contact(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     name = user_data.get('name')
#     button_text = message.text
#
#     if button_text == 'Finish':
#         await message.answer(
#             f'Now {name} has this data:\n' + print_contact_by_name(name),
#             reply_markup=make_main_menu()
#         )
#         await state.clear()
#         return
#
#     if button_text.lower() in contact_fields:
#         await message.answer(
#             f'Type new {button_text.lower()}:',
#             reply_markup=ReplyKeyboardRemove()
#         )
#         await state.update_data(field_to_update=button_text.lower())
#         await state.set_state(EditContactState.waiting_for_data)
#         return
#
#     await message.answer("Error. Choose menu option.", reply_markup=make_edit_user_menu())
#
#
# @router.message(EditContactState.waiting_for_data)
# async def update_field_value(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     field_to_update: str = user_data.get('field_to_update')
#     if field_to_update == 'name':
#         await state.update_data(name=message.text)
#
#     if field_to_update:
#         id = user_data.get('id')
#         contact = requests.put(f'{BASE_URL}/contacts/{id}', data=json.dumps({field_to_update: message.text})).json()
#         print(contact)
#         await message.answer(
#             f"{field_to_update.capitalize()} changed to {contact[field_to_update]}.",
#             reply_markup=make_edit_user_menu()
#         )
#         await state.set_state(EditContactState.waiting_for_choosing_what_to_edit)
#         return
#
#     await message.answer("Error", reply_markup=make_edit_user_menu())
