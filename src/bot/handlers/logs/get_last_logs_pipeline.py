from aiogram.enums import ParseMode
from aiogram.types import Message



async def get_last_logs(message: Message):
    # TODO имплиментировать
    # text = await Helper.get_last_logs()
    await message.answer(
        "Need to implement",
        parse_mode=ParseMode.MARKDOWN_V2,
    )
