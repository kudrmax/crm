from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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


def make_row_keyboard_by_list(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_log_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Start logging"),
                KeyboardButton(text="Get log"),
                KeyboardButton(text="Exit"),
            ]
        ],
        resize_keyboard=True,
    )
