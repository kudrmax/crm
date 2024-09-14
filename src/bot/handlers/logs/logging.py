from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.common.logging import start_logging
from src.bot.keyboards.keyboards import make_log_menu_kb
from src.bot.states.states import AddLog

router = Router()


@router.message(AddLog.menu, F.text == 'Start logging')
async def get_logs(message: Message, state: FSMContext):
    await start_logging(
        message=message,
        state=state,
        final_state=AddLog.menu,
        final_reply_markup=make_log_menu_kb(),
    )
