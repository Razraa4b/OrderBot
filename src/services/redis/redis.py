from typing import Any, List
import redis.asyncio as redis


class Redis:
    def __init__(self, url: str) -> None:
        self._redis = redis.from_url(url)

    async def set(self, key: str, value: Any, ex: int | None = None) -> None:
        async with self._redis.pipeline() as pipe:
            pipe.set(key, value, ex=ex)
            await pipe.execute()

    async def get(self, key: str) -> Any:
        async with self._redis.pipeline() as pipe:
            pipe.get(key)
            result = await pipe.execute()
            return result

    async def push(self, key: str, ex: int | None = None, *values) -> None:
        async with self._redis.pipeline() as pipe:
            await pipe.rpush(key, *values)
            if ex:
                await pipe.expire(key, ex)
            await pipe.execute()

    async def lrange(self, key: str, start: int, end: int) -> List[Any]:
        async with self._redis.pipeline() as pipe:
            await pipe.lrange(key, start, end)
            result = await pipe.execute()
            if isinstance(result, list):
                return result[0]
            return result
