import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()


async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set in .env")

    bot = Bot(token=token)

    # На всякий случай отключаем webhook (если вдруг когда-то включался)
    await bot.delete_webhook(drop_pending_updates=True)

    # И дополнительно чистим очередь апдейтов
    await bot.get_updates(offset=-1)

    await bot.session.close()
    print("OK: webhook deleted, pending updates dropped.")


if __name__ == "__main__":
    asyncio.run(main())
