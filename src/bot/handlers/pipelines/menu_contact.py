from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards import contact_profile_kb
from src.bot.states import ContactProfileState


async def start_menu_contact_pipeline(
        message: Message,
        state: FSMContext,
        text: str | None = "Choose action",
        reply_markup: FSMContext | None = contact_profile_kb(),
):
    await message.answer(text, reply_markup=reply_markup)
    await state.set_state(ContactProfileState.choose_action)