from abc import ABC, abstractmethod
from decimal import Decimal


class PriceProvider(ABC):
    @abstractmethod
    async def get_price(self, ticker: str) -> Decimal:
        pass