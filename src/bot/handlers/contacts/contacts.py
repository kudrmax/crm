from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


from src.bot.contact_helper import ContactHelper

router = Router()


def make_contacts_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Find contacts"),
                KeyboardButton(text="Create new contact"),
                KeyboardButton(text="Go to main menu"),
            ]
        ],
        resize_keyboard=True,
    )


@router.message(StateFilter(None), F.text == 'Contacts')
async def menu_contacts(message: Message):
    await message.answer(
        'Choose action:',
        reply_markup=make_contacts_menu_kb()
    )
