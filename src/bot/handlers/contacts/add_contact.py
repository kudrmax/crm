from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.contact_helper import ContactHelper
from src.bot.handlers.contacts.keyboards import make_contacts_menu_kb
from src.bot.handlers.contacts.states import AddContactState

router = Router()


@router.message(StateFilter(None), F.text == 'Create new contact')
async def create_contact(message: Message, state: FSMContext):
    await message.answer(
        'Type name:',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddContactState.name)


@router.message(AddContactState.name)
async def set_name(message: Message, state: FSMContext):
    name = message.text
    if not await ContactHelper.add_new_contact(name):
        await message.answer(
            f'Contact {name} already exists. Type another name:',
        )
    else:
        await message.answer(
            f'Contact {name} was added',
            reply_markup=make_contacts_menu_kb()
        )
        await state.clear()
