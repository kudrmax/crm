from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.contacts.search_contact_pipeline import search_contact
from src.bot.keyboards import main_kb, contact_profile_kb, make_row_keyboard_by_list
from src.bot.states import ContactProfileState, AddContactState

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Choose option:", reply_markup=main_kb())


@router.message(F.text == 'Go to main menu')
async def go_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Choose option:", reply_markup=main_kb())


@router.message(StateFilter(None), F.text == 'Find contact')
async def find_contact(message: Message, state: FSMContext):
    await search_contact(
        message=message,
        state=state,
        start_state=None,
        start_reply_markup=main_kb(),
        final_state=ContactProfileState.choose_action,
        final_reply_markup=contact_profile_kb(),
    )


@router.message(StateFilter(None), F.text == 'Get last logs')
async def get_last_logs(message: Message, state: FSMContext):
    pass


@router.message(StateFilter(None), F.text == 'Create new contact')
async def create_contact(message: Message, state: FSMContext):
    await message.answer(
        'Type name:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(AddContactState.name)
