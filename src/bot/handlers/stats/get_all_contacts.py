from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.bot.states import StatsState
from src.services.contact_log.service import contact_log_service
from src.services.telegram.service import telegram_service

router = Router()


@router.message(StatsState.menu, F.text.lower().contains('all contacts'))
async def get_all_contacts(message: Message, state: FSMContext):
    contacts = contact_log_service.get_all_contacts()
    text = telegram_service.get_all_contacts_post(contacts)
    # text = await Helper.get_all_contacts()
    await message.answer(
        text,
        # parse_mode=ParseMode.MARKDOWN_V2,
    )
