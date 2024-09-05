from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.keyboards.yes_or_no import get_yes_no_kb

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Вопрос после старта",
        reply_markup=get_yes_no_kb()
    )


@router.message(F.text.lower() == "да")
async def answer_yes(message: Message):
    await message.answer(
        "Вы ответили да",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text.lower() == "нет")
async def answer_no(message: Message):
    await message.answer(
        "Вы ответили нет",
        reply_markup=ReplyKeyboardRemove()
    )
