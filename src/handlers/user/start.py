from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from services.database.context import DatabaseContext
from services.database.models import User, UserBotSettings

from keyboards.reply import main_keyboard


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, context: DatabaseContext) -> None:
    await message.answer("👋Hi, this is a bot for tracking new orders from new exchanges! " \
                         "I'll notify you of new posts so you can be the first to pick them up⚡️",
                         reply_markup=main_keyboard)
    
    telegram_id = message.from_user.id
    # if user not exists, create him    
    user: User = await context.get(User, User.telegram_id == telegram_id)
    if not user:
        new_user = User(telegram_id=telegram_id)
        new_user.bot_settings = UserBotSettings()
        await context.add(new_user)
