from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards.keyboards import make_contacts_menu_kb
from src.bot.states.states import ContactProfileState

router = Router()


@router.message(StateFilter(None), F.text == 'Contacts')
async def menu_contacts(message: Message, state: FSMContext):
    await message.answer(
        'Choose action:',
        reply_markup=make_contacts_menu_kb()
    )
