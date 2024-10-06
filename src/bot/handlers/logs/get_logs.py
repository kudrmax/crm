from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.common.get_logs import get_logs
from src.bot.states import AddLog

router = Router()


@router.message(AddLog.menu, F.text == 'Get logs')
async def get_logs_handler(message: Message, state: FSMContext):
    await get_logs(message, state)
