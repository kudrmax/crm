from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.bot.states import StatsState

router = Router()


@router.message(StatsState.menu, F.text.lower().contains('with days'))
async def who(message: Message, state: FSMContext):
    text = await Helper.get_days_count_since_last_interaction()
    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2)
