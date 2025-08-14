from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.balance import Balance


class BalanceRepository(ABC):
    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> Optional[Balance]:
        pass

    @abstractmethod
    async def create(self, balance: Balance) -> Balance:
        pass

    @abstractmethod
    async def update(self, balance: Balance) -> Balance:
        pass