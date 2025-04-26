from aiogram import Bot

from services.database.context import DatabaseContext
from services.database.models import User, UserBotSettings


async def start_mailing(bot: Bot, context: DatabaseContext) -> None:
    pass
