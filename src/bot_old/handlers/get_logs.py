# import requests
# from aiogram import types, Router, F
# from aiogram.filters import StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import ReplyKeyboardRemove
#
# from src.bot.common import BASE_URL, print_contact_by_name
# from src.bot_old.handlers.main import make_main_menu
# from src.bot_old.keyboards.simple_row_by_list import make_row_keyboard_by_list
#
# router = Router()
#
# class GetLogState(StatesGroup):
#     waiting_for_typing_name = State()
#     waiting_for_choosing_name = State()
#     waiting_for_choosing_what_to_edit = State()
#     waiting_for_data = State()
#
#
# # def make_edit_user_menu():
# #     return make_row_keyboard_by_list([
# #         *[w.capitalize() for w in contact_fields],
# #         'Finish',
# #     ])
#
#
# @router.message(StateFilter(None), F.text == 'Get logs')
# async def get_contact_name(message: types.Message, state: FSMContext):
#     await message.answer("Type contact name:", reply_markup=ReplyKeyboardRemove())
#     await state.set_state(GetLogState.waiting_for_typing_name)
#
#
# @router.message(GetLogState.waiting_for_typing_name)
# async def edit_contact(message: types.Message, state: FSMContext):
#     name = message.text
#     contacts = (requests.get(f'{BASE_URL}/contacts/search/{name}')).json()
#     contact_names = [contact['name'] for contact in contacts]
#     await message.answer(
#         'Choose contact',
#         reply_markup=make_row_keyboard_by_list(contact_names)
#     )
#     await state.set_state(GetLogState.waiting_for_choosing_name)
#
#
# @router.message(GetLogState.waiting_for_choosing_name)
# async def edit_contact(message: types.Message, state: FSMContext):
#     name = message.text
#     contact = requests.get(f'{BASE_URL}/contacts/name/{name}')
#     await state.update_data(name=name)
#     id = contact.json().get('id')
#     await state.update_data(id=id)
#     await message.answer(
#         f'You are editing {name}:\n' + print_contact_by_name(name)
#     )
#     logs = requests.get(f'{BASE_URL}/logs/{id}').json()
#     await message.answer(
#         f'Log of contact {name}:\n' + '\n'.join(['- ' + log['log'] for log in logs]),
#         reply_markup=make_main_menu()
#     )
#     await state.clear()