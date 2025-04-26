from typing import List

import asyncio
from aiogram import Bot

from services.database.context import DatabaseContext
from services.database.models import User


async def send_mail(bot: Bot, user: User) -> None:
    await bot.send_message(user.telegram_id, "Hello")


async def start_mailing(bot: Bot, context: DatabaseContext | None) -> None:
    users: List[User] = await context.get_all(User, True, [User.bot_settings])
    tasks = []
    for user in users:
        if user.bot_settings.is_enabled:
            tasks.append(asyncio.create_task(send_mail(bot, user)))
    await asyncio.gather(*tasks)
