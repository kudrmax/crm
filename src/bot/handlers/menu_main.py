from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.contacts.search_contact_pipeline import search_contact
from src.bot.handlers.logs.get_last_logs_pipeline import get_last_logs
from src.bot.keyboards import main_kb, contact_profile_kb, make_row_keyboard_by_list, make_keyboard_by_lists, stats_kb
from src.bot.states import ContactProfileState, AddContactState, StatsState

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Choose option:", reply_markup=main_kb())


@router.message(F.text.lower().contains('go to main menu'))
async def go_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Choose option:", reply_markup=main_kb())


@router.message(StateFilter(None), F.text.lower().contains('find contact'))
async def find_contact(message: Message, state: FSMContext):
    await search_contact(
        message=message,
        state=state,
        start_state=None,
        start_reply_markup=main_kb(),
        final_state=ContactProfileState.choose_action,
        final_reply_markup=contact_profile_kb(),
    )


@router.message(StateFilter(None), F.text.lower().contains('get last logs'))
async def get_last_logs_handler(message: Message, state: FSMContext):
    await get_last_logs(message)


@router.message(StateFilter(None), F.text.lower().contains('create new contact'))
async def create_contact(message: Message, state: FSMContext):
    await message.answer(
        'Type name:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(AddContactState.name)


@router.message(StateFilter(None), F.text.lower().contains('Stats'))
async def get_stats(message: Message, state: FSMContext):
    await state.set_state(StatsState.menu)
    await message.answer(
        'Choose option:',
        reply_markup=stats_kb()
    )
