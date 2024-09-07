from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from src.bot.keyboards.simple_row_by_list import make_row_keyboard_by_list

router = Router()


def make_main_menu():
    return make_row_keyboard_by_list([
        'Add log',
        'Add contact',
        'Edit contact',
        'Get logs',
        'Get stats',
    ])


@router.message(StateFilter(None), Command("start"))
async def start_command(message: Message):
    await message.answer("Choose option:", reply_markup=make_main_menu())
