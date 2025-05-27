import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from db import engine
from config import TELEGRAM_TOKEN
from handlers import dp
from middlewares import SubscriptionMiddleware
import models
import logging

LOG_FORMAT = "[%(asctime)s] %(levelname)s | %(name)s | %(message)s"

logging.basicConfig(
    level=logging.INFO, filemode="a", filename="bot.logs", format=LOG_FORMAT
)

logging.getLogger("aiogram").setLevel(logging.ERROR)


bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ),
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def main():
    await init_db()
    logging.info("Database initialized successfully.")
    logging.info("Starting Telegram Bot...")
    dp.message.middleware(SubscriptionMiddleware())

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.error(e)
        logging.info("Stopping bot due to an error.")


if __name__ == "__main__":
    asyncio.run(main())
