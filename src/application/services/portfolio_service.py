from typing import List
from src.domain.entities.stock_balance import StockBalance
from src.domain.repositories.stock_balance_repository import StockBalanceRepository


class PortfolioService:
    def __init__(self, stock_balance_repository: StockBalanceRepository):
        self.stock_balance_repository = stock_balance_repository

    async def get_portfolio(self, user_id: str) -> List[StockBalance]:
        return await self.stock_balance_repository.find_by_user_id(user_id)