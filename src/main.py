import logging
from sys import stdout

import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.config import Configuration
from services.mailing import start_mailing
from middlewares import ConfigurationMiddleware, DatabaseMiddleware

from handlers.user import start, commands


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG, stream=stdout)

    bot = Bot(token=Configuration().get_token())
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()

    config_middleware = ConfigurationMiddleware()
    db_middleware = DatabaseMiddleware()

    await db_middleware.create_context(connection_string=config_middleware.get_config().get_db_connection_string())

    scheduler.add_job(start_mailing, trigger="interval", seconds=10,
                      kwargs={
                          "bot": bot, "context": db_middleware.get_context()
                      })
    scheduler.start()

    dp.update.middleware(config_middleware)
    dp.update.middleware(db_middleware)

    dp.include_router(start.router)
    dp.include_router(commands.router)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await db_middleware.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Telegram bot stopped...")
 