from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.stock_balance import StockBalance


class StockBalanceRepository(ABC):
    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[StockBalance]:
        pass

    @abstractmethod
    async def find_by_user_id_and_ticker(self, user_id: str, ticker: str) -> Optional[StockBalance]:
        pass

    @abstractmethod
    async def create(self, stock_balance: StockBalance) -> StockBalance:
        pass

    @abstractmethod
    async def update(self, stock_balance: StockBalance) -> StockBalance:
        pass

    @abstractmethod
    async def delete(self, stock_balance_id: str) -> None:
        pass