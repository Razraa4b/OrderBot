import logging
import asyncio
from sys import stdout
from aiogram import Bot, Dispatcher

from services.config import Configuration
from middlewares import ConfigurationMiddleware, DatabaseMiddleware

from handlers.user import start, commands


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG, stream=stdout)

    bot = Bot(token=Configuration().get_token())
    dp = Dispatcher()

    db_middleware = DatabaseMiddleware()

    dp.update.middleware(ConfigurationMiddleware())
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
 