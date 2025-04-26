from typing import Callable, Dict, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message

from services.config import Configuration
from services.database.context import DatabaseContext


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self._context = None

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # create db context if it not created
        if not self._context:
            config: Configuration = data["config"]
            self._context = await DatabaseContext.create(config.get_db_connection_string(),
                                                         True)
        data['context'] = self._context
        return await handler(event, data)
    
    async def dispose(self) -> None:
        if self._context:
            await self._context.dispose()
