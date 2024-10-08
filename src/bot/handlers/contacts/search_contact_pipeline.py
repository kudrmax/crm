from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message

from src.bot.helper import Helper
from src.bot.keyboards import make_row_keyboard_by_list, make_keyboard_by_lists
from src.bot.states import FindContactState
from src.errors import ContactNotFoundError

router = Router()


async def search_contact(
        message: Message,
        state: FSMContext,
        final_state: StatesGroup | None,
        start_state: StatesGroup | None,
        final_reply_markup,
        start_reply_markup,
):
    await state.update_data(final_state=final_state)
    await state.update_data(start_state=start_state)
    await state.update_data(final_reply_markup=final_reply_markup)
    await state.update_data(start_reply_markup=start_reply_markup)
    last_contacts = await Helper.get_last_contacts()
    await state.update_data(last_contacts=set(last_contacts))

    await message.answer(
        'Type name or select from list:',
        reply_markup=make_keyboard_by_lists([*[[contact] for contact in last_contacts], ['Cancel']])
    )
    await state.set_state(FindContactState.typing_name)


async def set_start_state(message: Message, state: FSMContext, text: str):
    data = await state.get_data()
    start_reply_markup = data['start_reply_markup']
    start_state = data['start_state']

    await message.answer(
        text,
        reply_markup=start_reply_markup
    )
    if not start_state:
        await state.clear()
    else:
        await state.set_state(start_state)


async def set_last_state(message: Message, state: FSMContext, name: str):
    try:
        contact_data = await Helper.get_contact_data_by_name(name)
    except ContactNotFoundError:
        await message.answer(f"Contact with name {name} not found")
        raise

    state_data = await state.get_data()
    final_state = state_data.get('final_state')
    final_reply_markup = state_data.get('final_reply_markup')

    contact_data_answer = await Helper.convert_contact_data_to_string(contact_data)
    await message.answer(
        contact_data_answer,
        reply_markup=final_reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.update_data(name=name)
    await state.set_state(final_state)


@router.message(FindContactState.typing_name, F.text.lower().contains('cancel'))
async def cancel(message: Message, state: FSMContext):
    await set_start_state(message, state, 'Canceled')


@router.message(FindContactState.typing_name)
async def contact(message: Message, state: FSMContext):
    name = message.text
    data = await state.get_data()
    last_contacts = data['last_contacts'] if 'last_contacts' in data else []

    if name in last_contacts:
        await set_last_state(message, state, name)
    else:
        await message.answer(f"Searching contact with name {name}")
        similar_contacts = await Helper.find_contacts_by_name(name)
        if similar_contacts is None:
            await set_start_state(message, state, 'Something went wrong. Error with similar contacts.')
        if len(similar_contacts) == 0:
            await message.answer("No contacts found. Type another name or cancel.")
            return
        buttons = similar_contacts + ['Cancel']
        await message.answer(
            'Choose contact from list:',
            reply_markup=make_row_keyboard_by_list(buttons)
        )
        await state.set_state(FindContactState.choosing_name_from_list)


@router.message(FindContactState.choosing_name_from_list, F.text.lower().contains('cancel'))
async def cancel(message: Message, state: FSMContext):
    await set_start_state(message, state, 'Canceled')


@router.message(FindContactState.choosing_name_from_list)
async def contact(message: Message, state: FSMContext):
    name = message.text
    await set_last_state(message, state, name)
