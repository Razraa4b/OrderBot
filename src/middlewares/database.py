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
        data['context'] = self._context
        return await handler(event, data)
    
    async def create_context(self, connection_string: str) -> None:
        # create db context if it not created
        if not self._context:
            config: Configuration = connection_string
            self._context = await DatabaseContext.create(connection_string, True)

    def get_context(self) -> DatabaseContext | None:
        return self._context
    
    async def dispose(self) -> None:
        if self._context:
            await self._context.dispose()
