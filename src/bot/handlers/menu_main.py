from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards import make_row_keyboard_by_list

router = Router()


def make_main_menu_kb():
    return make_row_keyboard_by_list([
        'Add log',
        'Contacts',
        'Get stats ❌',
    ])


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Choose option:", reply_markup=make_main_menu_kb())


@router.message(F.text == 'Go to main menu')
async def go_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Choose option:", reply_markup=make_main_menu_kb())
