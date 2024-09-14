from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.common.get_logs import get_logs
from src.bot.handlers.common.logging import start_logging
from src.bot.keyboards.keyboards import make_edit_contact_kb, make_contact_profile_kb
from src.bot.states.states import ContactProfileState, EditContactState
from src.bot.handlers.menu_main import make_main_menu_kb

router = Router()


@router.message(ContactProfileState.choose_action, F.text == 'Get logs')
async def get_logs_handler(message: Message, state: FSMContext):
    await get_logs(message, state)


@router.message(ContactProfileState.choose_action, F.text == 'Start logging')
async def add_log(message: Message, state: FSMContext):
    await start_logging(
        message=message,
        state=state,
        final_state=ContactProfileState.choose_action,
        final_reply_markup=make_contact_profile_kb(),
    )


@router.message(ContactProfileState.choose_action, F.text == 'Edit contact')
async def edit_contact(message: Message, state: FSMContext):
    await message.answer(
        'Choose what to edit:',
        reply_markup=make_edit_contact_kb()
    )
    await state.set_state(EditContactState.choose_what_edit)


@router.message(ContactProfileState.choose_action, F.text == 'Delete contact log')
async def delete_contact(message: Message, state: FSMContext):
    pass


@router.message(ContactProfileState.choose_action, F.text == 'Go to main menu')
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Choose option:',
        reply_markup=make_main_menu_kb()
    )
