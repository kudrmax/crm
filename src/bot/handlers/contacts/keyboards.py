from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.bot.keyboards.simple_row_by_list import make_row_keyboard_by_list


def make_process_contact_kb():
    return make_row_keyboard_by_list([
        'Get log ❌',
        'Add log ❌',
        'Edit contact',
        'Delete contact ❌',
        'Exit',
    ])


def make_edit_contact_kb():
    return make_row_keyboard_by_list([
        *[w.capitalize() for w in contact_fields],
        'Finish',
    ])


def make_contacts_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Find contact"),
                KeyboardButton(text="Create new contact"),
                KeyboardButton(text="Go to main menu"),
            ]
        ],
        resize_keyboard=True,
    )


contact_fields: List[str] = [
    'name',
    'telegram',
    'phone',
    'birthday',
]
