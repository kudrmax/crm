import asyncio

from aiogram import Bot, Dispatcher
from decouple import config

from handlers.main import router as main_router
from handlers.add_contact import router as add_contact_router
from handlers.edit_contact import router as edit_contact_router

TOKEN = config("BOT_TOKEN")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(
        main_router,
        add_contact_router,
        edit_contact_router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
