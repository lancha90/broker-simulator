from typing import List
from decimal import Decimal
from datetime import datetime
import uuid
import logging

from src.domain.entities.trade import Trade, TradeType
from src.domain.repositories.trade_repository import TradeRepository
from src.infrastructure.config.postgres_database import postgres_db

logger = logging.getLogger(__name__)


class PostgresTradeRepository(TradeRepository):
    def __init__(self):
        self.table_name = "ibkr_trades"

    async def create(self, trade: Trade) -> Trade:
        connection = await postgres_db.get_connection()
        try:
            # Generate UUID if not provided
            trade_id = trade.id or str(uuid.uuid4())
            now = datetime.utcnow()

            query = f"""
                INSERT INTO {self.table_name} (id, user_id, ticker, trade_type, quantity, price, total_amount, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id, user_id, ticker, trade_type, quantity, price, total_amount, created_at
            """

            logger.debug(f"[PostgresTradeRepository:create] - Creating trade [user_id={trade.user_id}, ticker={trade.ticker}, type={trade.trade_type}]")

            row = await connection.fetchrow(
                query,
                trade_id,
                trade.user_id,
                trade.ticker,
                trade.trade_type.value,
                float(trade.quantity),
                float(trade.price),
                float(trade.total_amount),
                now
            )

            logger.info(f"[PostgresTradeRepository:create] - Trade created [id={row['id']}, user_id={row['user_id']}, ticker={row['ticker']}, type={row['trade_type']}]")

            return Trade(
                id=row['id'],
                user_id=row['user_id'],
                ticker=row['ticker'],
                trade_type=TradeType(row['trade_type']),
                quantity=Decimal(str(row['quantity'])),
                price=Decimal(str(row['price'])),
                total_amount=Decimal(str(row['total_amount'])),
                created_at=row['created_at']
            )
        except Exception as e:
            logger.error(f"[PostgresTradeRepository:create] - Error creating trade [user_id={trade.user_id}, ticker={trade.ticker}, error={str(e)}]")
            raise
        finally:
            await postgres_db.release_connection(connection)

    async def find_by_user_id(self, user_id: str) -> List[Trade]:
        try:
            connection = await postgres_db.get_connection()
            try:
                query = f"""
                    SELECT id, user_id, ticker, trade_type, quantity, price, total_amount, created_at
                    FROM {self.table_name}
                    WHERE user_id = $1
                    ORDER BY created_at DESC
                """
                logger.debug(f"[PostgresTradeRepository:find_by_user_id] - Executing query [user_id={user_id}]")

                rows = await connection.fetch(query, user_id)

                trades = [
                    Trade(
                        id=row['id'],
                        user_id=row['user_id'],
                        ticker=row['ticker'],
                        trade_type=TradeType(row['trade_type']),
                        quantity=Decimal(str(row['quantity'])),
                        price=Decimal(str(row['price'])),
                        total_amount=Decimal(str(row['total_amount'])),
                        created_at=row['created_at']
                    )
                    for row in rows
                ]

                logger.debug(f"[PostgresTradeRepository:find_by_user_id] - Found {len(trades)} trades [user_id={user_id}]")
                return trades
            finally:
                await postgres_db.release_connection(connection)
        except Exception as e:
            logger.error(f"[PostgresTradeRepository:find_by_user_id] - Error finding trades [user_id={user_id}, error={str(e)}]")
            return []
