from decimal import Decimal
from typing import Optional
from src.application.ports.cache import Cache
from src.application.ports.price_provider import PriceProvider
from src.domain.entities.stock_price import StockPrice
from datetime import datetime


class PriceService:
    def __init__(self, price_provider: PriceProvider, cache: Cache):
        self.price_provider = price_provider
        self.cache = cache
        self.cache_ttl = 180

    async def get_current_price(self, ticker: str) -> Optional[StockPrice]:
        cache_key = f"price:{ticker}"
        
        cached_price = await self.cache.get(cache_key)
        if cached_price:
            return StockPrice(**cached_price)

        price = await self.price_provider.get_price(ticker)
        if price:
            stock_price = StockPrice(
                ticker=ticker,
                price=price,
                source="external",
                timestamp=datetime.now()
            )
            await self.cache.set(cache_key, stock_price.model_dump(), self.cache_ttl)
            return stock_price
        
        return None