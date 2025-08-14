from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.trade import Trade


class TradeRepository(ABC):
    @abstractmethod
    async def create(self, trade: Trade) -> Trade:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Trade]:
        pass