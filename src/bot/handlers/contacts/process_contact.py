from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.common.get_logs import get_logs
from src.bot.handlers.common.logging import start_logging
from src.bot.helper import Helper
from src.bot.keyboards import make_edit_contact_kb, make_contact_profile_kb, make_row_keyboard_by_list
from src.bot.states import ContactProfileState, EditContactState, DeleteContactState, EditLogsState
from src.bot.handlers.menu_main import make_main_menu_kb
from src.errors import ContactNotFoundError

router = Router()


@router.message(ContactProfileState.choose_action, F.text == 'Get logs ⬇️')
async def get_logs_handler(message: Message, state: FSMContext):
    await get_logs(message, state)


@router.message(ContactProfileState.choose_action, F.text == 'Я')
async def get_logs_handler(message: Message, state: FSMContext):
    await get_logs(message, state, name='Я')


@router.message(ContactProfileState.choose_action, F.text == 'Start logging ⬆️')
async def add_log(message: Message, state: FSMContext):
    await get_logs(message, state)
    await start_logging(
        message=message,
        state=state,
        final_state=ContactProfileState.choose_action,
        final_reply_markup=make_contact_profile_kb(),
    )


@router.message(ContactProfileState.choose_action, F.text == 'Add empty log')
async def add_empty_log(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        await Helper.add_empty_log(name=data['name'])
        await message.answer('Interaction was added.')
    except ContactNotFoundError:
        await message.answer(f"Contact with name {data['name']} not found. Aborted.")
        raise


@router.message(ContactProfileState.choose_action, F.text == 'Edit contact')
async def edit_contact(message: Message, state: FSMContext):
    await message.answer(
        'Choose what to edit:',
        reply_markup=make_edit_contact_kb()
    )
    await state.set_state(EditContactState.choose_what_edit)


@router.message(ContactProfileState.choose_action, F.text == 'Delete contact')
async def delete_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    await state.set_state(DeleteContactState.waiting_confirmation)
    await message.answer(
        f'Type "I want to delete contact {name}" to delete contact {name}.',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )


@router.message(ContactProfileState.choose_action, F.text == 'Go to main menu')
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Choose option:',
        reply_markup=make_main_menu_kb()
    )
