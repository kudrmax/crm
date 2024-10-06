from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.common.search_contact import search_contact
from src.bot.keyboards import make_contact_profile_kb, make_contacts_menu_kb
from src.bot.states import ContactProfileState

router = Router()


@router.message(StateFilter(None), F.text == 'Find contact')
async def find_contact(message: Message, state: FSMContext):
    await search_contact(
        message=message,
        state=state,
        start_state=None,
        start_reply_markup=make_contacts_menu_kb(),
        final_state=ContactProfileState.choose_action,
        final_reply_markup=make_contact_profile_kb(),
    )
