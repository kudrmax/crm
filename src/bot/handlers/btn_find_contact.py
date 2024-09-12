from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.contact_helper import ContactHelper
from src.bot.handlers.search_contact import search_contact
from src.bot.keyboards.keyboards import make_process_contact_kb, make_contacts_menu_kb, make_row_keyboard_by_list
from src.bot.states.states import ProcessContactState, FindContactState
from src.bot.handlers.menu_main import make_main_menu

router = Router()


@router.message(StateFilter(None), F.text == 'Find contact')
async def find_contact(message: Message, state: FSMContext):
    await search_contact(
        message,
        state,
        next_state=ProcessContactState.choose_action,
        cancel_state=None,
        reply_markup=make_process_contact_kb(),
    )
