from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.pipelines.create_contact import start_create_contact_pipeline
from src.bot.handlers.pipelines.search_contact import start_search_contact_pipeline
from src.bot.handlers.logs.get_last_logs_pipeline import get_last_logs
from src.bot.keyboards import main_kb, contact_profile_kb, stats_kb
from src.bot.states import ContactProfileState, StatsState

router = Router()


async def start_main_menu_pipeline(
        message: Message,
        state: FSMContext,
        text: str | None = "Choose action",
        reply_markup: FSMContext | None = main_kb(),
):
    await message.answer(text, reply_markup=reply_markup)
    await state.clear()


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
    await start_search_contact_pipeline(
        message=message,
        state=state,
        start_state=None,
        start_reply_markup=main_kb(),
        final_state=ContactProfileState.choose_action,
        final_reply_markup=contact_profile_kb(),
    )


@router.message(StateFilter(None), F.text.lower().contains('last logs'))
async def get_last_logs_handler(message: Message, state: FSMContext):
    await get_last_logs(message)


@router.message(StateFilter(None), F.text.lower().contains('new contact'))
async def create_contact(message: Message, state: FSMContext):
    await start_create_contact_pipeline(message, state)


@router.message(StateFilter(None), F.text.lower().contains('stats'))
async def get_stats(message: Message, state: FSMContext):
    await state.set_state(StatsState.menu)
    await message.answer(
        'Choose option:',
        reply_markup=stats_kb()
    )
