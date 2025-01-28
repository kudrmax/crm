from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.orm.base import state_str

from src.bot.keyboards import contact_profile_kb, edit_contact_kb
from src.bot.states import ContactProfileState, EditContactState
from src.errors import ContactNotFoundError, UnprocessableEntityError, AlreadyExistsError, NotFoundError, \
    ContactAlreadyExistsErr
from src.models.contact.model import MContactUpdate
from src.services.contact_log.service import contact_log_service

router = Router()


@router.message(EditContactState.choose_what_edit, F.text.lower().contains('finish'))
async def choose_action(message: Message, state: FSMContext):
    name = (await state.get_data()).get('name')
    try:
        contact = contact_log_service.get_contact_by_name(name)
    except ContactNotFoundError:
        await message.answer(f"Contact with name {name} not found")
        raise

    contact_str = contact.to_string()
    await message.answer(
        contact_str,
        # parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=contact_profile_kb()
    )
    await state.set_state(ContactProfileState.choose_action)


@router.message(EditContactState.choose_what_edit)
async def choose_action(message: Message, state: FSMContext):
    def get_filed_from_button_text(button_text: str):
        if 'name' in button_text.lower():
            return 'name'
        if 'telegram' in button_text.lower():
            return 'telegram'
        if 'phone' in button_text.lower():
            return 'phone'
        if 'birthday' in button_text.lower():
            return 'birthday'
        return None

    button_text = message.text
    field = get_filed_from_button_text(button_text)
    if not field:
        await message.answer(f"You should press a button, not type text. Choose one of the buttons:")
        return

    await message.answer(
        f"Type new {field}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(field_to_update=field)
    await state.set_state(EditContactState.waiting_for_data)


@router.message(EditContactState.waiting_for_data)
async def update_field_value(message: Message, state: FSMContext):
    state_data = await state.get_data()
    field_to_update = state_data.get('field_to_update')
    name = state_data.get('name')

    new_value = message.text

    contact = contact_log_service.get_contact_by_name(name)
    contact_update = MContactUpdate()

    if field_to_update == 'name':
        contact_update.name = new_value
        old_value = contact.name
    elif field_to_update == 'telegram':
        contact_update.telegram = new_value
        old_value = contact.telegram
    elif field_to_update == 'phone':
        contact_update.phone = new_value
        old_value = contact.phone
    elif field_to_update == 'birthday':
        contact_update.birthday = new_value
        old_value = contact.birthday
    else:
        raise Exception(f'Unknown field {field_to_update}')

    try:
        contact_log_service.update_contact_by_name(name, contact_update)
        if field_to_update == 'name':
            await state.update_data(name=new_value)

    except ContactAlreadyExistsErr:
        await message.answer(f"Contact with name {message.text} already exists. Type another name:")
        return
    except UnprocessableEntityError:
        if field_to_update != 'birthday':
            raise
        await message.answer(f'A date should be in the format "YYYY-MM-DD". Type another date:')
        return

    await message.answer(
        f"You changed **{field_to_update}** of **{name}** from **{old_value}** to **{new_value}**",
        reply_markup=edit_contact_kb()
    )
    await state.set_state(EditContactState.choose_what_edit)
