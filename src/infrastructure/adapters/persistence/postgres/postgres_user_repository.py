from typing import Optional
from datetime import datetime
import uuid
import logging

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.config.postgres_database import postgres_db

logger = logging.getLogger(__name__)


class PostgresUserRepository(UserRepository):
    def __init__(self):
        self.table_name = "ibkr_users"

    async def find_by_api_key(self, api_key: str) -> Optional[User]:
        try:
            connection = await postgres_db.get_connection()
            try:
                query = f"SELECT id, email, api_key, created_at, updated_at FROM {self.table_name} WHERE api_key = $1"
                logger.debug(f"[PostgresUserRepository:find_by_api_key] - Executing query [api_key={api_key[:8]}...]")

                row = await connection.fetchrow(query, api_key)

                if row:
                    return User(
                        id=row['id'],
                        email=row['email'],
                        api_key=row['api_key'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )

                logger.debug(f"[PostgresUserRepository:find_by_api_key] - User not found [api_key={api_key[:8]}...]")
                return None
            finally:
                await postgres_db.release_connection(connection)
        except Exception as e:
            logger.error(f"[PostgresUserRepository:find_by_api_key] - Error finding user [api_key={api_key[:8]}..., error={str(e)}]")
            return None

    async def create(self, user: User) -> User:
        connection = await postgres_db.get_connection()
        try:
            # Generate UUID if not provided
            user_id = user.id or str(uuid.uuid4())
            now = datetime.utcnow()

            query = f"""
                INSERT INTO {self.table_name} (id, email, api_key, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, email, api_key, created_at, updated_at
            """

            logger.debug(f"[PostgresUserRepository:create] - Creating user [email={user.email}]")

            row = await connection.fetchrow(
                query,
                user_id,
                user.email,
                user.api_key,
                now,
                now
            )

            logger.info(f"[PostgresUserRepository:create] - User created [id={row['id']}, email={row['email']}]")

            return User(
                id=row['id'],
                email=row['email'],
                api_key=row['api_key'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        except Exception as e:
            logger.error(f"[PostgresUserRepository:create] - Error creating user [email={user.email}, error={str(e)}]")
            raise
        finally:
            await postgres_db.release_connection(connection)

    async def find_by_id(self, user_id: str) -> Optional[User]:
        try:
            connection = await postgres_db.get_connection()
            try:
                query = f"SELECT id, email, api_key, created_at, updated_at FROM {self.table_name} WHERE id = $1"
                logger.debug(f"[PostgresUserRepository:find_by_id] - Executing query [user_id={user_id}]")

                row = await connection.fetchrow(query, user_id)

                if row:
                    return User(
                        id=row['id'],
                        email=row['email'],
                        api_key=row['api_key'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )

                logger.debug(f"[PostgresUserRepository:find_by_id] - User not found [user_id={user_id}]")
                return None
            finally:
                await postgres_db.release_connection(connection)
        except Exception as e:
            logger.error(f"[PostgresUserRepository:find_by_id] - Error finding user [user_id={user_id}, error={str(e)}]")
            return None
