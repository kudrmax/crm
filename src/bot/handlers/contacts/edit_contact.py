from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.helper import ContactHelper
from src.bot.keyboards.keyboards import make_contact_profile_kb, make_edit_contact_kb, contact_fields
from src.bot.states.states import ContactProfileState, EditContactState
from src.errors import *

router = Router()


@router.message(EditContactState.choose_what_edit, F.text == 'Finish')
async def choose_action(message: Message, state: FSMContext):
    name = (await state.get_data()).get('name')
    try:
        contact_data = await ContactHelper.get_contact_data_by_name(name)
    except ContactNotFoundError:
        await message.answer(f"Contact with name {name} not found")
        raise

    contact_for_print = await ContactHelper.print_contact_data(contact_data)
    await message.answer(
        f'Updated contact {name}\n' + contact_for_print,
        reply_markup=make_contact_profile_kb(),
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
        updated_data = await ContactHelper.update_contact(name, field_to_update, new_data)
        if field_to_update == 'name':
            await state.update_data(name=message.text)
        await message.answer(
            f'You changed filed "{updated_data['field']}" from "{updated_data['old_value']}" to "{updated_data['new_value']}"',
            reply_markup=make_edit_contact_kb()
        )
        await state.set_state(EditContactState.choose_what_edit)
    except ContactNotFoundError:
        await message.answer(f'Contact with name {name} not found. Aborted.')
        raise Exception
    except ContactAlreadyExistsError:
        await message.answer(f"Contact with name {message.text} already exists. Type another name:")
        return
