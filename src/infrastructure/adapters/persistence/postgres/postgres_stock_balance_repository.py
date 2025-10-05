from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid
import logging

from src.domain.entities.stock_balance import StockBalance
from src.domain.repositories.stock_balance_repository import StockBalanceRepository
from src.infrastructure.config.postgres_database import postgres_db

logger = logging.getLogger(__name__)


class PostgresStockBalanceRepository(StockBalanceRepository):
    def __init__(self):
        self.table_name = "ibkr_stock_balances"

    async def find_by_user_id(self, user_id: str) -> List[StockBalance]:
        try:
            connection = await postgres_db.get_connection()
            try:
                query = f"SELECT id, user_id, ticker, quantity, average_price, current_price, created_at, updated_at FROM {self.table_name} WHERE user_id = $1"
                logger.debug(f"[PostgresStockBalanceRepository:find_by_user_id] - Executing query [user_id={user_id}]")

                rows = await connection.fetch(query, user_id)

                stock_balances = [
                    StockBalance(
                        id=row['id'],
                        user_id=row['user_id'],
                        ticker=row['ticker'],
                        quantity=Decimal(str(row['quantity'])),
                        average_price=Decimal(str(row['average_price'])),
                        current_price=Decimal(str(row['current_price'])),
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                    for row in rows
                ]

                logger.debug(f"[PostgresStockBalanceRepository:find_by_user_id] - Found {len(stock_balances)} stock balances [user_id={user_id}]")
                return stock_balances
            finally:
                await postgres_db.release_connection(connection)
        except Exception as e:
            logger.error(f"[PostgresStockBalanceRepository:find_by_user_id] - Error finding stock balances [user_id={user_id}, error={str(e)}]")
            return []

    async def find_by_user_id_and_ticker(self, user_id: str, ticker: str) -> Optional[StockBalance]:
        try:
            connection = await postgres_db.get_connection()
            try:
                query = f"SELECT id, user_id, ticker, quantity, average_price, current_price, created_at, updated_at FROM {self.table_name} WHERE user_id = $1 AND ticker = $2"
                logger.debug(f"[PostgresStockBalanceRepository:find_by_user_id_and_ticker] - Executing query [user_id={user_id}, ticker={ticker}]")

                row = await connection.fetchrow(query, user_id, ticker)

                if row:
                    return StockBalance(
                        id=row['id'],
                        user_id=row['user_id'],
                        ticker=row['ticker'],
                        quantity=Decimal(str(row['quantity'])),
                        average_price=Decimal(str(row['average_price'])),
                        current_price=Decimal(str(row['current_price'])),
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )

                logger.debug(f"[PostgresStockBalanceRepository:find_by_user_id_and_ticker] - Stock balance not found [user_id={user_id}, ticker={ticker}]")
                return None
            finally:
                await postgres_db.release_connection(connection)
        except Exception as e:
            logger.error(f"[PostgresStockBalanceRepository:find_by_user_id_and_ticker] - Error finding stock balance [user_id={user_id}, ticker={ticker}, error={str(e)}]")
            return None

    async def create(self, stock_balance: StockBalance) -> StockBalance:
        connection = await postgres_db.get_connection()
        try:
            # Generate UUID if not provided
            stock_balance_id = stock_balance.id or str(uuid.uuid4())
            now = datetime.utcnow()

            query = f"""
                INSERT INTO {self.table_name} (id, user_id, ticker, quantity, average_price, current_price, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id, user_id, ticker, quantity, average_price, current_price, created_at, updated_at
            """

            logger.debug(f"[PostgresStockBalanceRepository:create] - Creating stock balance [user_id={stock_balance.user_id}, ticker={stock_balance.ticker}]")

            row = await connection.fetchrow(
                query,
                stock_balance_id,
                stock_balance.user_id,
                stock_balance.ticker,
                float(stock_balance.quantity),
                float(stock_balance.average_price),
                float(stock_balance.current_price),
                now,
                now
            )

            logger.info(f"[PostgresStockBalanceRepository:create] - Stock balance created [id={row['id']}, user_id={row['user_id']}, ticker={row['ticker']}]")

            return StockBalance(
                id=row['id'],
                user_id=row['user_id'],
                ticker=row['ticker'],
                quantity=Decimal(str(row['quantity'])),
                average_price=Decimal(str(row['average_price'])),
                current_price=Decimal(str(row['current_price'])),
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        except Exception as e:
            logger.error(f"[PostgresStockBalanceRepository:create] - Error creating stock balance [user_id={stock_balance.user_id}, ticker={stock_balance.ticker}, error={str(e)}]")
            raise
        finally:
            await postgres_db.release_connection(connection)

    async def update(self, stock_balance: StockBalance) -> StockBalance:
        connection = await postgres_db.get_connection()
        try:
            now = datetime.utcnow()

            query = f"""
                UPDATE {self.table_name}
                SET quantity = $1, average_price = $2, current_price = $3, updated_at = $4
                WHERE id = $5
                RETURNING id, user_id, ticker, quantity, average_price, current_price, created_at, updated_at
            """

            logger.debug(f"[PostgresStockBalanceRepository:update] - Updating stock balance [id={stock_balance.id}]")

            row = await connection.fetchrow(
                query,
                float(stock_balance.quantity),
                float(stock_balance.average_price),
                float(stock_balance.current_price),
                now,
                stock_balance.id
            )

            if not row:
                error_msg = f"Stock balance not found [id={stock_balance.id}]"
                logger.error(f"[PostgresStockBalanceRepository:update] - {error_msg}")
                raise ValueError(error_msg)

            logger.info(f"[PostgresStockBalanceRepository:update] - Stock balance updated [id={row['id']}, ticker={row['ticker']}]")

            return StockBalance(
                id=row['id'],
                user_id=row['user_id'],
                ticker=row['ticker'],
                quantity=Decimal(str(row['quantity'])),
                average_price=Decimal(str(row['average_price'])),
                current_price=Decimal(str(row['current_price'])),
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        except Exception as e:
            logger.error(f"[PostgresStockBalanceRepository:update] - Error updating stock balance [id={stock_balance.id}, error={str(e)}]")
            raise
        finally:
            await postgres_db.release_connection(connection)

    async def delete(self, stock_balance_id: str) -> None:
        connection = await postgres_db.get_connection()
        try:
            query = f"DELETE FROM {self.table_name} WHERE id = $1"
            logger.debug(f"[PostgresStockBalanceRepository:delete] - Deleting stock balance [id={stock_balance_id}]")

            result = await connection.execute(query, stock_balance_id)

            logger.info(f"[PostgresStockBalanceRepository:delete] - Stock balance deleted [id={stock_balance_id}]")
        except Exception as e:
            logger.error(f"[PostgresStockBalanceRepository:delete] - Error deleting stock balance [id={stock_balance_id}, error={str(e)}]")
            raise
        finally:
            await postgres_db.release_connection(connection)
