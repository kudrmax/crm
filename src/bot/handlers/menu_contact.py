from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.pipelines.contact_delete import start_delete_contact_pipeline
from src.bot.handlers.pipelines.contact_profile_get import start_get_profile_pipeline
from src.bot.handlers.pipelines.contact_serach import search_contact_from_main_to_profile
from src.bot.handlers.pipelines.logs_get import start_get_logs_pipeline
from src.bot.handlers.pipelines.logs_logging import start_logging
from src.bot.keyboards import edit_contact_kb, contact_profile_kb, main_kb
from src.bot.states import ContactProfileState, EditContactState
from src.errors import ContactNotFoundError
from src.models.contact.model import MContactCreate
from src.models.log.models import MLogCreate
from src.services.contact_log.service import contact_log_service

router = Router()


@router.message(ContactProfileState.choose_action, F.text.lower().contains('profile'))
async def get_profile(message: Message, state: FSMContext):
    await start_get_profile_pipeline(message, state)


@router.message(ContactProfileState.choose_action, F.text.lower().contains('get logs'))
async def get_logs_handler(message: Message, state: FSMContext):
    await start_get_logs_pipeline(message, state)


@router.message(ContactProfileState.choose_action, F.text == 'Я')
async def get_logs_handler(message: Message, state: FSMContext):
    contact = contact_log_service.get_contact_by_name('Я')
    if not contact:
        contact_log_service.create_contact(MContactCreate(name='Я'))
    await start_get_logs_pipeline(message, state, name='Я')
    await state.update_data(logs_are_got=False)


@router.message(ContactProfileState.choose_action, F.text.lower().contains('start logging'))
async def add_log(message: Message, state: FSMContext):
    data = await state.get_data()
    if 'logs_are_got' not in data or 'logs_are_got' in data and data['logs_are_got'] == False:
        await start_get_logs_pipeline(message, state)
    await start_logging(
        message=message,
        state=state,
        final_state=ContactProfileState.choose_action,
        final_reply_markup=contact_profile_kb(),
    )


@router.message(ContactProfileState.choose_action, F.text.lower().contains('add empty log'))
async def add_empty_log(message: Message, state: FSMContext):
    await state.update_data(logs_are_got=False)
    data = await state.get_data()
    try:
        contact = contact_log_service.get_contact_by_name(data['name'])
        contact_log_service.create_log(MLogCreate(
            contact_id=contact.id,
            text="",
        ))
        # await Helper.add_empty_log(name=data['name'])
        await message.answer('Interaction was added.')
    except ContactNotFoundError:
        await message.answer(f"Contact with name {data['name']} not found. Aborted.")
        raise


@router.message(ContactProfileState.choose_action, F.text.lower().contains('edit contact'))
async def edit_contact(message: Message, state: FSMContext):
    await state.update_data(logs_are_got=False)
    await message.answer(
        'Choose what to edit:',
        reply_markup=edit_contact_kb()
    )
    await state.set_state(EditContactState.choose_what_edit)


@router.message(ContactProfileState.choose_action, F.text.lower().contains('delete contact'))
async def delete_contact(message: Message, state: FSMContext):
    await start_delete_contact_pipeline(message, state)


@router.message(ContactProfileState.choose_action, F.text.lower().contains('find contact'))
async def find_contact(message: Message, state: FSMContext):
    await state.clear()
    await search_contact_from_main_to_profile(message, state)


@router.message(ContactProfileState.choose_action, F.text.lower().contains('go to main menu'))
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Choose option:',
        reply_markup=main_kb()
    )
