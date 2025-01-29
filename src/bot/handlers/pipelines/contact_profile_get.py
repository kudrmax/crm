from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards import contact_profile_kb
from src.bot.states import ContactProfileState
from src.errors import ContactNotFoundErr, NameNotFoundInState
from src.services.contact_log.service import contact_log_service


async def start_get_profile_pipeline(message: Message, state: FSMContext):
    data = await state.get_data()

    name = data.get('name')
    if not name:
        raise ContactNotFoundErr()

    contact = contact_log_service.get_contact_by_name(name)
    if not contact:
        raise NameNotFoundInState()

    contact_str = contact.to_string()

    await message.answer(
        contact_str,
        reply_markup=contact_profile_kb()
    )

    await state.set_state(ContactProfileState.choose_action)
    await state.update_data(logs_are_got=False)
