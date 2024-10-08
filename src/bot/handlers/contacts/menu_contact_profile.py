from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.logs.get_logs_pipeline import get_logs
from src.bot.handlers.logs.logging_pipeline import start_logging
from src.bot.helper import Helper
from src.bot.keyboards import edit_contact_kb, contact_profile_kb, make_row_keyboard_by_list, \
    main_kb
from src.bot.states import ContactProfileState, EditContactState, DeleteContactState
from src.errors import ContactNotFoundError

router = Router()


@router.message(ContactProfileState.choose_action, F.text.lower().contains('profile'))
async def get_profile(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    contact_data = await Helper.get_contact_data_by_name(name)
    contact_data_answer = await Helper.convert_contact_data_to_string(contact_data)
    await message.answer(contact_data_answer, parse_mode=ParseMode.MARKDOWN_V2)


@router.message(ContactProfileState.choose_action, F.text.lower().contains('get logs'))
async def get_logs_handler(message: Message, state: FSMContext):
    await get_logs(message, state)


@router.message(ContactProfileState.choose_action, F.text == 'Я')
async def get_logs_handler(message: Message, state: FSMContext):
    await get_logs(message, state, name='Я')


@router.message(ContactProfileState.choose_action, F.text.lower().contains('start logging'))
async def add_log(message: Message, state: FSMContext):
    await get_logs(message, state)
    await start_logging(
        message=message,
        state=state,
        final_state=ContactProfileState.choose_action,
        final_reply_markup=contact_profile_kb(),
    )


@router.message(ContactProfileState.choose_action, F.text.lower().contains('add empty log'))
async def add_empty_log(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        await Helper.add_empty_log(name=data['name'])
        await message.answer('Interaction was added.')
    except ContactNotFoundError:
        await message.answer(f"Contact with name {data['name']} not found. Aborted.")
        raise


@router.message(ContactProfileState.choose_action, F.text.lower().contains('edit contact'))
async def edit_contact(message: Message, state: FSMContext):
    await message.answer(
        'Choose what to edit:',
        reply_markup=edit_contact_kb()
    )
    await state.set_state(EditContactState.choose_what_edit)


@router.message(ContactProfileState.choose_action, F.text.lower().contains('delete contact'))
async def delete_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    await state.set_state(DeleteContactState.waiting_confirmation)
    await message.answer(
        f'Type "I want to delete contact {name}" to delete contact {name}.',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )


@router.message(ContactProfileState.choose_action, F.text.lower().contains('go to main menu'))
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Choose option:',
        reply_markup=main_kb()
    )
