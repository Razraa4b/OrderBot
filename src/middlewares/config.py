from typing import Callable, Dict, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message

from services.config import Configuration


class ConfigurationMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self._config = Configuration()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data['config'] = self._config
        return await handler(event, data)
