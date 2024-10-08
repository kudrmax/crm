from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.errors import ContactNotFoundError


async def get_logs(message: Message, state: FSMContext, name: str | None = None):
    data = await state.get_data()
    if not name:
        name = data.get('name')
    try:
        all_logs, _ = await Helper.get_all_logs(name)
        if Helper.text_is_empty(all_logs):
            await message.answer(f'👎🏻 There is no logs for {name}')
            return
        await message.answer(
            Helper.create_str_for_logs(all_logs, name),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    except ContactNotFoundError:
        await message.answer(f"Contact with name {name} not found.")
