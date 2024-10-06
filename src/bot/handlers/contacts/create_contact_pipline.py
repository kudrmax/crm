from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.bot.keyboards import make_row_keyboard_by_list, main_kb
from src.bot.states import AddContactState
from src.errors import ContactAlreadyExistsError

router = Router()


@router.message(AddContactState.name, F.text == 'Cancel')
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
        await Helper.create_contact(name)
        await message.answer(
            f'Contact {name} was added',
            reply_markup=main_kb()
        )
        await state.clear()
    except ContactAlreadyExistsError:
        await message.answer(f'Contact {name} already exists. Type another name:')
