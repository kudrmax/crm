from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard_by_list(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_keyboard_by_lists(items: list[list[str]]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками на основе списка списков.
    :param items: список списков текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    keyboard = [
        [KeyboardButton(text=item) for item in row]
        for row in items
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def main_kb():
    return make_keyboard_by_lists([
        ['Find contact 🔎', 'Last logs ⬇️'],
        ['New contact 🆕', 'Stats 📈']
    ])


def contact_profile_kb():
    return make_keyboard_by_lists([
        ['Start logging ⬆️', 'Get logs ⬇️', 'Я'],
        ['Edit log', 'Delete log', 'Add empty log'],
        ['Edit contact', 'Delete contact', 'Go to main menu']
    ])


def edit_log_kb():
    return make_row_keyboard_by_list([
        'Edit text',
        'Edit date',
        'Cancel',
    ])


def edit_contact_kb():
    return make_keyboard_by_lists([
        *[[w.capitalize()] for w in contact_fields],
        ['Finish'],
    ])


def stats_kb():
    return make_keyboard_by_lists([
        ['Get all contacts'],
        ['Go to main menu']
    ])


contact_fields: List[str] = [
    'name',
    'telegram',
    'phone',
    'birthday',
]
