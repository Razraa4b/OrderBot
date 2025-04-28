from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message
from aiogram.exceptions import TelegramForbiddenError

from services.database.context import DatabaseContext
from services.database.models import User


router = Router()


@router.error(ExceptionTypeFilter(TelegramForbiddenError))
async def handle_forbidden_error(event: ErrorEvent, context: DatabaseContext) -> None:
    telegram_id = event.update.message.from_user.id
    await context.delete(User, User.telegram_id == telegram_id)
