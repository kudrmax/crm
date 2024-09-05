from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_new_data_or_change_name_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить новые данные")
    kb.button(text="Изменить имя")
    kb.button(text="Завершить")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
