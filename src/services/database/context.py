from typing import List, Any, Optional, Sequence
from .models import Base

from sqlalchemy import update, select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker, 
                                    AsyncSession, AsyncEngine)


class DatabaseContext:
    @classmethod
    async def create(cls, connection_string: str, echo: bool = False) -> "DatabaseContext":
        self = cls()

        self._engine = create_async_engine(connection_string, echo=echo)

        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        self._session_maker = async_sessionmaker(bind=self._engine)

        return self
    
    async def add(self, entity: Base) -> None:
        async with self._session_maker() as session:
            session.add(entity)
            await session.commit()

    async def get(self, entity_type: type, condition: Any, relationships: List[Any] = []) -> Optional[Base]:
        query = select(entity_type).where(condition)
        if relationships:
            query = query.options(*[joinedload(rel) for rel in relationships])
        async with self._session_maker() as session:
            result = await session.execute(query)
            entity = result.scalars().first()
            return entity
        
    async def get_all(self, entity_type: type, condition: Any, relationships: List[Any] = []) -> Sequence[Base]:
        query = select(entity_type).where(condition)
        if relationships:
            query = query.options(*[joinedload(rel) for rel in relationships])
        async with self._session_maker() as session:
            result = await session.execute(query)
            entity = result.scalars().all()
            return entity
        
    async def delete(self, entity_type: type, condition: Any) -> None:
        query = delete(entity_type).where(condition)
        async with self._session_maker() as session:
            await session.execute(query)
            await session.commit()
    
    async def update(self, entity_type: type, condition: Any, **kwargs) -> None:
        query = update(entity_type).where(condition).values(kwargs)
        async with self._session_maker() as session:
            await session.execute(query)
            await session.commit()

    async def dispose(self) -> None:
        await self._engine.dispose()
