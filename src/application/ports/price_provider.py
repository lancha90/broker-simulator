from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional, Tuple


class PriceProvider(ABC):
    @abstractmethod
    async def get_price(self, ticker: str) -> Optional[Tuple[Decimal, str]]:
        pass