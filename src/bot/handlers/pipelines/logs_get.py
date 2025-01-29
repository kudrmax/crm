from typing import List

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup

from src.models.log.models import MLogWithNumbers
from src.services.contact_log.service import contact_log_service
from src.services.telegram.service import telegram_service


async def start_get_logs_pipeline(
        message: Message,
        state: FSMContext,
        logs: List[MLogWithNumbers] | None = None,
        name: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None
):
    name = name if name else (await state.get_data()).get('name')

    if not logs:
        logs: List[MLogWithNumbers] = contact_log_service.get_logs_by_contact_name(name, need_numbers=True)
    logs_str = telegram_service.get_logs_post(logs, name=name)

    await message.answer(
        logs_str,
        # parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )

    await state.update_data(logs_are_got=True)
