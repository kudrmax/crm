import asyncio

from aiogram import Bot, Dispatcher

from src.bot.routers import router
from src.settings import settings


async def main():
    bot = Bot(token=settings.telegram_bot.token)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    print('Bot is running.')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
