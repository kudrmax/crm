# import requests
# from aiogram import types
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram import Router
#
# from src.bot.common import BASE_URL, print_contact_by_name
# from src.bot_old.handlers.edit_contact import make_edit_user_menu
#
# router = Router()
#
#
# class ContactState(StatesGroup):
#     waiting_for_name = State()
#
#
# @router.message(ContactState.waiting_for_name)
# async def edit_contact(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     name = data['name'] if 'name' in data else message.text
#     contact = requests.get(f'{BASE_URL}/contacts/name/{name}')
#     await state.update_data(name=name)
#     await state.update_data(id=contact.json().get('id'))
#     await message.answer(
#         f'You are editing {name}:\n' + print_contact_by_name(name),
#         reply_markup=make_edit_user_menu()
#     )
#     # await state.set_state(EditContactState.waiting_for_choosing_what_to_edit)
