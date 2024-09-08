import asyncio

from aiogram import Bot, Dispatcher
from decouple import config

from src.bot.handlers.main_menu import router as main_router
from src.bot.handlers.contacts import router as contact_router
# from src.bot_old.handlers.add_contact import router as add_contact_router
# from src.bot_old.handlers.edit_contact import router as edit_contact_router
# from src.bot_old.handlers.get_logs import router as logs_router

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
