import asyncio

from aiogram import Bot, Dispatcher
from decouple import config

from src.bot.handlers.menu_main import router as main_router
from src.bot.routers import router as contact_router

TOKEN = config("BOT_TOKEN")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(
        main_router,
        contact_router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
