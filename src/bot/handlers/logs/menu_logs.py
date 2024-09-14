from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.menu_main import make_main_menu_kb
from src.bot.handlers.common.search_contact import search_contact
from src.bot.states.states import AddLog
from src.bot.keyboards.keyboards import make_log_menu_kb

router = Router()


@router.message(StateFilter(None), F.text == 'Add log')
async def log_menu(message: Message, state: FSMContext):
    await search_contact(
        message=message,
        state=state,
        start_state=None,
        start_reply_markup=make_main_menu_kb(),
        final_state=AddLog.menu,
        final_reply_markup=make_log_menu_kb(),
    )


@router.message(AddLog.menu, F.text == 'Go to main menu')
async def go_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Choose option:", reply_markup=make_main_menu_kb())

