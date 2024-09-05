import asyncio

from aiogram import Bot, Dispatcher
from decouple import config

from handlers.main import router as main_router

TOKEN = config("BOT_TOKEN")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)
    # dp.include_router(users.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
