from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.contact_helper import ContactHelper
from src.bot.handlers.contacts.keyboards import make_process_contact_kb
from src.bot.handlers.contacts.states import ProcessContactState, FindContactState
from src.bot.handlers.main_menu import make_main_menu
from src.bot.keyboards.simple_row_by_list import make_row_keyboard_by_list

router = Router()


@router.message(StateFilter(None), F.text == 'Find contact')
async def find_contact(message: Message, state: FSMContext):
    await message.answer(
        'Type name:',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FindContactState.type_name)


@router.message(FindContactState.type_name)
async def choose_name(message: Message, state: FSMContext):
    name = message.text
    await message.answer(f"Searching contact with name {name}")
    similar_contacts = await ContactHelper.find_contact_by_name(name)
    print(f'{similar_contacts = }')

    if similar_contacts is None:
        await message.answer(
            "Something went wrong.",
            reply_markup=make_main_menu()
        )
        await state.clear()
        return

    if len(similar_contacts) == 0:
        await message.answer(
            "No contacts found. Type another name or cancel.",
            reply_markup=make_row_keyboard_by_list(['Cancel'])
        )
        return

    buttons = similar_contacts + ['Cancel']
    await message.answer(
        'Choose contact from list',
        reply_markup=make_row_keyboard_by_list(buttons)
    )
    await state.set_state(FindContactState.choose_name)


@router.message(FindContactState.choose_name)
async def contact(message: Message, state: FSMContext):
    name = message.text
    contact_data = await ContactHelper.get_contact_data_by_name(name)

    if not contact_data:
        await message.answer(
            "Something went wrong.",
            reply_markup=make_main_menu()
        )
        await state.clear()
        return

    answer = await ContactHelper.print_contact_data(contact_data)
    await message.answer(f'Contact info for {name}')
    await message.answer(
        answer,
        reply_markup=make_process_contact_kb()
    )
    await state.set_state(ProcessContactState.choose_action)
    await state.update_data(name=name)
