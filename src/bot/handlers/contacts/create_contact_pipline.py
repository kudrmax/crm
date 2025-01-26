from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper, ContactHelper, contact_helper
from src.bot.keyboards import make_row_keyboard_by_list, main_kb
from src.bot.states import AddContactState
from src.errors import ContactAlreadyExistsError, AlreadyExistsError, ContactAlreadyExistsErr
from src.services.contact_log.service import ContactLogService, new_contact_service
from src.storage.postgres.connection.engine import engine
from src.storage.postgres.repositories.contacts.repository import ContactRepository

router = Router()


@router.message(AddContactState.name, F.text.lower().contains('сancel'))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Canceled",
        reply_markup=main_kb()
    )


@router.message(AddContactState.name)
async def set_name(message: Message, state: FSMContext):
    name = message.text
    try:
        await contact_helper.create_contact(name)
        await message.answer(
            f'Contact {name} was added',
            reply_markup=main_kb()
        )
        await state.clear()
    except ContactAlreadyExistsErr:
        await message.answer(f'Contact {name} already exists. Type another name:')
