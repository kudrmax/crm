import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from decouple import config

TOKEN = config("BOT_TOKEN")

# logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")

@dp.message(Command("test2"))
async def cmd_test2(message: types.Message):
    await message.reply("Test 2")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
