import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from decouple import config

TOKEN = config("BOT_TOKEN")

# logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=TOKEN,
    # default=DefaultBotProperties(
    #     parse_mode=ParseMode.MARKDOWN_V2
    # )
)
dp = Dispatcher()


@dp.message(F.text, Command("text"))
async def cmd_text(message: types.Message):
    await message.answer(
        "Просто текст"
    )
    await message.answer(
        """
        *2024\-01\-01*
        \- Некий текст
        \- Некий текст
        """,
        parse_mode=ParseMode.MARKDOWN_V2
    )


@dp.message(Command('hello'))
async def cmd_hello(message: types.Message):
    await message.answer(f'Hello, {message.from_user.first_name} (@{message.from_user.username})!')


async def main():
    await dp.start_polling(bot)


# class ButtonsEnum(Enum):
#     main_menu = "Главное меню"
#     add_log = "Добавить лог"
#     add_user = "Добавить пользователя"
#     edit_user = "Редактировать пользователя"
#     get_stats = "Получить статистику"
#
#
# TOKEN = config("BOT_TOKEN")
#
# logging.basicConfig(level=logging.INFO)
#
#
# @dp.message(Command("button"))
# async def cmd_button(message: types.Message):
#     kb = [
#         [
#             types.KeyboardButton(text=ButtonsEnum.add_log.value),
#             types.KeyboardButton(text="Добавить пользователя"),
#             types.KeyboardButton(text="Редактировать пользователя"),
#             types.KeyboardButton(text="Получить статистику"),
#         ]
#     ]
#     keyboard = types.ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True,
#         input_field_placeholder="Подсказка на клавиатуре",
#         one_time_keyboard=True
#     )
#     await message.answer("Выберите действие", reply_markup=keyboard)
#
#
# @dp.message(F.text == ButtonsEnum.add_log.value)
# async def with_puree(message: types.Message):
#     await message.reply("Лог добавлен")

if __name__ == "__main__":
    asyncio.run(main())
