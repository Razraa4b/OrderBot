from abc import ABC, abstractmethod


@ABC
class Parser[T]:
    async def parse() -> T:
        pass
