import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from src.application.ports.cache import Cache


class MemoryCache(Cache):
    def __init__(self):
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if datetime.now() < expiry:
                    return value
                else:
                    del self._cache[key]
            return None

    async def set(self, key: str, value: Any, ttl_seconds: int = 180) -> None:
        async with self._lock:
            expiry = datetime.now() + timedelta(seconds=ttl_seconds)
            self._cache[key] = (value, expiry)

    async def delete(self, key: str) -> None:
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def cleanup_expired(self):
        async with self._lock:
            now = datetime.now()
            expired_keys = [k for k, (_, expiry) in self._cache.items() if now >= expiry]
            for key in expired_keys:
                del self._cache[key]