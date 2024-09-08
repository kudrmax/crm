from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from src.bot.keyboards.keyboards import make_row_keyboard_by_list

router = Router()


def make_main_menu():
    return make_row_keyboard_by_list([
        'Add log',
        'Contacts',
        'Get stats ❌',
    ])


@router.message(StateFilter(None), Command("start"))
async def start_command(message: Message):
    await message.answer("Choose option:", reply_markup=make_main_menu())


@router.message(StateFilter(None), F.text == 'Go to main menu')
async def go_to_main_menu(message: Message):
    await message.answer("Choose option:", reply_markup=make_main_menu())
