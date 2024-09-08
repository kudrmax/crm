# import requests
# from aiogram import types, F
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
# from aiogram.filters import StateFilter
# from aiogram import Router
#
# from src.bot.common import BASE_URL
# from src.bot_old.handlers.contact_main_menu import ContactState
# from src.bot_old.keyboards.simple_row_by_list import make_row_keyboard_by_list
#
# router = Router()
#
# keyboard_main = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text="Search contact")],
#     [KeyboardButton(text="Add new contact")]
# ], resize_keyboard=True)
#
#
# # Состояния
# class SearchOrCretaeContactState(StatesGroup):
#     choose_action = State()
#     search_contact = State()
#     search_contact_waiting_for_choosing_from_list = State()
#     add_contact = State()
#
#
# @router.message(StateFilter(None), F.text == 'Add contact')
# async def get_contact_name(message: types.Message, state: FSMContext):
#     await message.answer("Выберите действие:", reply_markup=keyboard_main)
#     await state.set_state(SearchOrCretaeContactState.choose_action)
#
#
# @router.message(SearchOrCretaeContactState.choose_action)
# async def process_action_choice(message: types.Message, state: FSMContext):
#     match message.text:
#         case "Search contact":
#             await message.answer("Type name:")
#             await state.set_state(SearchOrCretaeContactState.search_contact)
#         case "Add new contact":
#             await message.answer("Type name:")
#             await state.set_state(SearchOrCretaeContactState.add_contact)
#         case _:
#             await message.answer("Please, press one of the buttons.")
#
#
# @router.message(SearchOrCretaeContactState.search_contact)
# async def process_search_contact(message: types.Message, state: FSMContext):
#     name = message.text
#     await message.answer(f"Searching contact with name {name}")
#     contacts = (requests.get(f'{BASE_URL}/contacts/search/{name}')).json()
#     contact_names = [contact['name'] for contact in contacts]
#     if len(contact_names) == 0:
#         await message.answer(
#             "No contacts found. Type another name or cancel.",
#             reply_markup=make_row_keyboard_by_list(['Cancel'])
#         )
#     else:
#         contact_names.append('Cancel')
#         await message.answer(
#             'Choose contact from list',
#             reply_markup=make_row_keyboard_by_list(contact_names)
#         )
#         await state.set_state(ContactState.waiting_for_name)
#
#
# @router.message(SearchOrCretaeContactState.add_contact)
# async def process_add_contact(message: types.Message, state: FSMContext):
#     name = message.text
#     res = requests.post(BASE_URL + '/contacts', data=json.dumps({"name": name}))
#     res_json = res.json()
#     await message.answer(f"User {res_json['name']} added")
#     await state.set_state(ContactState.waiting_for_name)
