from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from src.bot.contact_helper import ContactHelper
from src.bot.handlers.search_contact import search_contact
from src.bot.states.states import AddLog, FindContactState
from src.bot.keyboards.keyboards import make_row_keyboard_by_list, make_log_menu_kb

router = Router()


@router.message(StateFilter(None), F.text == 'Add log')
async def log_menu(message: Message, state: FSMContext):
    await search_contact(
        message,
        state,
        next_state=AddLog.menu,
        cancel_state=None,
        reply_markup=make_log_menu_kb(),
    )


@router.message(AddLog.menu, F.text == 'Get log')
async def add_log(message: Message, state: FSMContext):
    state_data = await state.get_data()
    name = state_data.get('name')
    all_logs = await ContactHelper.get_all_logs(name)
    if all_logs and all_logs != "":
        await message.answer(
            all_logs
        )
