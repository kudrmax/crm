from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.helper import Helper
from src.bot.keyboards import contact_profile_kb, edit_contact_kb, contact_fields
from src.bot.states import ContactProfileState, EditContactState
from src.errors import ContactNotFoundError, ContactAlreadyExistsError, UnprocessableEntityError, AlreadyExistsError, \
    NotFoundError

router = Router()


@router.message(EditContactState.choose_what_edit, F.text.lower().contains('finish'))
async def choose_action(message: Message, state: FSMContext):
    name = (await state.get_data()).get('name')
    try:
        contact_data = await Helper.get_contact_data_by_name(name)
    except ContactNotFoundError:
        await message.answer(f"Contact with name {name} not found")
        raise

    contact_data_answer = await Helper.convert_contact_data_to_string(contact_data)
    await message.answer(
        contact_data_answer,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=contact_profile_kb()
    )
    await state.set_state(ContactProfileState.choose_action)


@router.message(EditContactState.choose_what_edit)
async def choose_action(message: Message, state: FSMContext):
    button_text = message.text
    if button_text.lower() in contact_fields:
        await message.answer(f"Type new data for filed {button_text}", reply_markup=ReplyKeyboardRemove())
        await state.update_data(field_to_update=button_text.lower())
        await state.set_state(EditContactState.waiting_for_data)
    else:
        await message.answer(f"You can't change this field. Choose one of the buttons:")


@router.message(EditContactState.waiting_for_data)
async def update_field_value(message: Message, state: FSMContext):
    user_data = await state.get_data()
    field_to_update = user_data.get('field_to_update')
    name = user_data.get('name')
    new_data = message.text
    try:
        updated_data = await Helper.update_contact(name, field_to_update, new_data)
        if field_to_update == 'name':
            await state.update_data(name=message.text)
        await message.answer(
            "\n".join([
                f"Field: {updated_data['field']}",
                f"Old value: {updated_data['old_value']}",
                f"New value: {updated_data['new_value']}",
            ]),
            reply_markup=edit_contact_kb()
        )
        await state.set_state(EditContactState.choose_what_edit)
    except NotFoundError:
        await message.answer(f'Contact with name {name} not found. Aborted.')
        raise Exception
    except AlreadyExistsError:
        await message.answer(f"Contact with name {message.text} already exists. Type another name:")
        return
    except UnprocessableEntityError:
        # if field_to_update == 'date':
        await message.answer(f'A date should be in the format "YYYY-MM-DD". Type another date:')
        return
        # raise
