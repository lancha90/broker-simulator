from abc import ABC, abstractmethod
from typing import Any, Optional


class Cache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int = 180) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass