import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.core.config import load_settings
from src.bot.handlers import router as bot_router
from src.db.init_db import init_db


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    settings = load_settings()

    # Инициализируем БД ДО запуска polling
    await init_db()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(bot_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
