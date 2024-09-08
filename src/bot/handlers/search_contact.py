from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.contact_helper import ContactHelper
from src.bot.keyboards.keyboards import make_process_contact_kb, make_contacts_menu_kb, make_row_keyboard_by_list
from src.bot.states.states import ProcessContactState, FindContactState
from src.bot.handlers.menu_main import make_main_menu

router = Router()


async def search_contact(message: Message, state: FSMContext, next_state, reply_markup, cancel_state=None):
    """

    Parameters
    ----------
    message: contact name
    next_state: состояние, в которое нужно перейти после нахождения контакта
    cancel_state: состояние, в которое нужно прийти если поиск будет отменен
    """
    await state.update_data(next_state=next_state)
    await state.update_data(cancel_state=cancel_state)
    await state.update_data(reply_markup=reply_markup)
    await message.answer(
        'Type name:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(FindContactState.type_name)


@router.message(FindContactState.type_name)
async def contact(message: Message, state: FSMContext):
    name = message.text
    await message.answer(f"Searching contact with name {name}")

    similar_contacts = await ContactHelper.find_contact_by_name(name)

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

    state_data = await state.get_data()
    next_state = state_data.get('next_state')
    reply_markup = state_data.get('reply_markup')

    answer = await ContactHelper.print_contact_data(contact_data)
    await message.answer(f'Contact info for {name}')
    await message.answer(
        answer,
        reply_markup=reply_markup
    )

    await state.update_data(name=name)
    await state.set_state(next_state)
