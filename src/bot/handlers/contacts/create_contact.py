from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper.contact_helper import ContactHelper
from src.bot.keyboards.keyboards import make_contacts_menu_kb, make_row_keyboard_by_list
from src.bot.states.states import AddContactState

router = Router()


@router.message(StateFilter(None), F.text == 'Create new contact')
async def create_contact(message: Message, state: FSMContext):
    await message.answer(
        'Type name:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(AddContactState.name)


@router.message(AddContactState.name, F.text == 'Cancel')
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Canceled",
        reply_markup=make_contacts_menu_kb()
    )


@router.message(AddContactState.name)
async def set_name(message: Message, state: FSMContext):
    name = message.text
    if not await ContactHelper.create_contact(name):
        await message.answer(f'Contact {name} already exists. Type another name:')
        return

    await message.answer(
        f'Contact {name} was added',
        reply_markup=make_contacts_menu_kb()
    )
    await state.clear()
