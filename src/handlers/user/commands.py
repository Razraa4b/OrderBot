from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services.database.context import DatabaseContext
from services.database.models import User, UserBotSettings


router = Router()


@router.message(Command("active"))
async def cmd_active(message: Message, context: DatabaseContext) -> None:
    user: User = await context.get(User, User.telegram_id == message.from_user.id, [User.bot_settings])

    await context.update(UserBotSettings, UserBotSettings.user_id == user.id,
                         is_enabled=not user.bot_settings.is_enabled)

    if not user.bot_settings.is_enabled:
        await message.answer("Now the bot will send you notifications again✅")
    else:
        await message.answer("Now the bot will stop sending you notifications❌")
