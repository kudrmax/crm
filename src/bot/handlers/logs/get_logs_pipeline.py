from typing import List

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.errors import ContactNotFoundError
from src.models.log.models import MLogWithNumbers
from src.services.contact_log.service import contact_log_service
from src.services.telegram.service import telegram_service


async def get_logs(message: Message, state: FSMContext, name: str | None = None):
    data = await state.get_data()
    if not name:
        name = data.get('name')
    try:
        logs: List[MLogWithNumbers] = contact_log_service.get_logs_by_contact_name(name, need_numbers=True)
        # all_logs, _ = await Helper.get_all_logs(name)
        if len(logs) == 0:
            await message.answer(f'👎🏻 There is no logs for {name}')
            return

        await message.answer(
            telegram_service.get_logs_post(logs),
            # parse_mode=ParseMode.MARKDOWN_V2
        )
    except ContactNotFoundError:
        await message.answer(f"Contact with name {name} not found.")
