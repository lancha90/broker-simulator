from decimal import Decimal
from typing import List, Optional
from src.application.ports.price_provider import PriceProvider
from src.infrastructure.adapters.external.yahoo_price_provider import YahooPriceProvider
from src.infrastructure.adapters.external.alphavantage_price_provider import AlphavantageProvider


class CompositePriceProvider(PriceProvider):
    def __init__(self):
        self.providers: List[PriceProvider] = [
            YahooPriceProvider(),
            AlphavantageProvider()
        ]

    async def get_price(self, ticker: str) -> Optional[Decimal]:
        for provider in self.providers:
            try:
                price = await provider.get_price(ticker)
                if price is not None:
                    return price
            except Exception:
                continue
        return None