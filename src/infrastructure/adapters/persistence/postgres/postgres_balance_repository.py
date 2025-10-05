from typing import Optional
from decimal import Decimal
from datetime import datetime
import uuid
import logging

from src.domain.entities.balance import Balance
from src.domain.repositories.balance_repository import BalanceRepository
from src.infrastructure.config.postgres_database import postgres_db

logger = logging.getLogger(__name__)


class PostgresBalanceRepository(BalanceRepository):
    def __init__(self):
        self.table_name = "ibkr_balances"

    async def find_by_user_id(self, user_id: str) -> Optional[Balance]:
        try:
            connection = await postgres_db.get_connection()
            try:
                query = f"SELECT id, user_id, cash_balance, created_at, updated_at FROM {self.table_name} WHERE user_id = $1"
                logger.debug(f"[PostgresBalanceRepository:find_by_user_id] - Executing query [user_id={user_id}]")

                row = await connection.fetchrow(query, user_id)

                if row:
                    return Balance(
                        id=row['id'],
                        user_id=row['user_id'],
                        cash_balance=Decimal(str(row['cash_balance'])),
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )

                logger.debug(f"[PostgresBalanceRepository:find_by_user_id] - Balance not found [user_id={user_id}]")
                return None
            finally:
                await postgres_db.release_connection(connection)
        except Exception as e:
            logger.error(f"[PostgresBalanceRepository:find_by_user_id] - Error finding balance [user_id={user_id}, error={str(e)}]")
            return None

    async def create(self, balance: Balance) -> Balance:
        connection = await postgres_db.get_connection()
        try:
            # Generate UUID if not provided
            balance_id = balance.id or str(uuid.uuid4())
            now = datetime.utcnow()

            query = f"""
                INSERT INTO {self.table_name} (id, user_id, cash_balance, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, user_id, cash_balance, created_at, updated_at
            """

            logger.debug(f"[PostgresBalanceRepository:create] - Creating balance [user_id={balance.user_id}, cash_balance={balance.cash_balance}]")

            row = await connection.fetchrow(
                query,
                balance_id,
                balance.user_id,
                float(balance.cash_balance),
                now,
                now
            )

            logger.info(f"[PostgresBalanceRepository:create] - Balance created [id={row['id']}, user_id={row['user_id']}]")

            return Balance(
                id=row['id'],
                user_id=row['user_id'],
                cash_balance=Decimal(str(row['cash_balance'])),
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        except Exception as e:
            logger.error(f"[PostgresBalanceRepository:create] - Error creating balance [user_id={balance.user_id}, error={str(e)}]")
            raise
        finally:
            await postgres_db.release_connection(connection)

    async def update(self, balance: Balance) -> Balance:
        connection = await postgres_db.get_connection()
        try:
            now = datetime.utcnow()

            query = f"""
                UPDATE {self.table_name}
                SET cash_balance = $1, updated_at = $2
                WHERE id = $3
                RETURNING id, user_id, cash_balance, created_at, updated_at
            """

            logger.debug(f"[PostgresBalanceRepository:update] - Updating balance [id={balance.id}, cash_balance={balance.cash_balance}]")

            row = await connection.fetchrow(
                query,
                float(balance.cash_balance),
                now,
                balance.id
            )

            if not row:
                error_msg = f"Balance not found [id={balance.id}]"
                logger.error(f"[PostgresBalanceRepository:update] - {error_msg}")
                raise ValueError(error_msg)

            logger.info(f"[PostgresBalanceRepository:update] - Balance updated [id={row['id']}, user_id={row['user_id']}]")

            return Balance(
                id=row['id'],
                user_id=row['user_id'],
                cash_balance=Decimal(str(row['cash_balance'])),
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        except Exception as e:
            logger.error(f"[PostgresBalanceRepository:update] - Error updating balance [id={balance.id}, error={str(e)}]")
            raise
        finally:
            await postgres_db.release_connection(connection)
