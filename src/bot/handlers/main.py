from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.bot.keyboards.simple_row_by_list import make_row_keyboard_by_list

router = Router()


def make_main_menu():
    return make_row_keyboard_by_list([
        'Добавить лог',
        'Добавить пользователя',
        'Редактировать пользователя',
        'Получить статистику',
    ])


@router.message(Command('start'))
async def cmd_new_user(message: Message):
    await message.answer(
        text="Выберите действие",
        reply_markup=make_main_menu()
    )
