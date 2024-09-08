from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.contact_helper import ContactHelper
from src.bot.handlers.search_contact import search_contact
from src.bot.keyboards.keyboards import make_process_contact_kb, make_contacts_menu_kb, make_row_keyboard_by_list
from src.bot.states.states import ProcessContactState, FindContactState
from src.bot.handlers.menu_main import make_main_menu

router = Router()


@router.message(StateFilter(None), F.text == 'Find contact')
async def find_contact(message: Message, state: FSMContext):
    await search_contact(
        message,
        state,
        next_state=ProcessContactState.choose_action,
        cancel_state=None,
        reply_markup=make_process_contact_kb(),
    )


# @router.message(FindContactState.type_name, F.text == 'Cancel')
# async def cancel(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer(
#         "Canceled",
#         reply_markup=make_contacts_menu_kb()
#     )


# @router.message(FindContactState.type_name)
# async def choose_name(message: Message, state: FSMContext):
#     name = message.text
#     await message.answer(f"Searching contact with name {name}")
#     similar_contacts = await ContactHelper.find_contact_by_name(name)
#
#     if similar_contacts is None:
#         await message.answer(
#             "Something went wrong.",
#             reply_markup=make_main_menu()
#         )
#         await state.clear()
#         return
#
#     if len(similar_contacts) == 0:
#         await message.answer(
#             "No contacts found. Type another name or cancel.",
#             reply_markup=make_row_keyboard_by_list(['Cancel'])
#         )
#         return
#
#     buttons = similar_contacts + ['Cancel']
#     await message.answer(
#         'Choose contact from list',
#         reply_markup=make_row_keyboard_by_list(buttons)
#     )
#     await state.set_state(FindContactState.choose_name)
#
#
# @router.message(FindContactState.choose_name)
# async def contact(message: Message, state: FSMContext):
#     name = message.text
#     contact_data = await ContactHelper.get_contact_data_by_name(name)
#
#     if not contact_data:
#         await message.answer(
#             "Something went wrong.",
#             reply_markup=make_main_menu()
#         )
#         await state.clear()
#         return
#
#     answer = await ContactHelper.print_contact_data(contact_data)
#     await message.answer(f'Contact info for {name}')
#     await message.answer(
#         answer,
#         reply_markup=make_process_contact_kb()
#     )
#
#     state_data = await state.get_data()
#     state_after_search = state_data.get('state_after_search')
#     if state_after_search:
#         await state.set_state(state_after_search)
#     else:
#         await state.set_state(ProcessContactState.choose_action)
#     await state.update_data(name=name)
