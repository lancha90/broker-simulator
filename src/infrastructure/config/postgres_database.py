import asyncpg
from src.infrastructure.config.settings import settings


class PostgresDatabase:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Create connection pool"""
        self.pool = await asyncpg.create_pool(
            settings.database_url,
            min_size=2,
            max_size=10,
            command_timeout=60
        )

    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()

    async def get_connection(self):
        """Get a connection from the pool"""
        if not self.pool:
            await self.connect()
        return await self.pool.acquire()

    async def release_connection(self, connection):
        """Release a connection back to the pool"""
        await self.pool.release(connection)


postgres_db = PostgresDatabase()
