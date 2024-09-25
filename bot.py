import asyncio

from aiogram import Bot, Dispatcher

from src.bot.handlers.menu_main import router as main_router
from src.bot.error_handlers import router as errors_router
from src.bot.routers import router as contact_router
from src.settings import settings


async def main():
    bot = Bot(token=settings.telegram_bot.token)
    dp = Dispatcher()
    dp.include_routers(
        errors_router,
        main_router,
        contact_router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    print('Bot is running.')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
