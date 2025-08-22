from decimal import Decimal
from typing import Optional
from src.application.ports.cache import Cache
from src.application.ports.price_provider import PriceProvider
from src.domain.entities.stock_price import StockPrice
from datetime import datetime
from src.infrastructure.config.logging_config import get_logger

logger = get_logger(__name__)


class PriceService:
    def __init__(self, price_provider: PriceProvider, cache: Cache):
        self.price_provider = price_provider
        self.cache = cache
        self.cache_ttl = 180

    async def get_current_price(self, ticker: str) -> Optional[StockPrice]:
        logger.info(f"Fetching price for ticker: {ticker}")
        
        cache_key = f"price:{ticker}"
        
        cached_price = await self.cache.get(cache_key)
        if cached_price:
            logger.info(f"Price found in cache for {ticker}: {cached_price['price']}")
            return StockPrice(**cached_price)

        logger.info(f"Cache miss for {ticker}, fetching from external provider")
        result = await self.price_provider.get_price(ticker)
        
        if result:
            price, source = result
            stock_price = StockPrice(
                ticker=ticker,
                price=price,
                source=source,
                timestamp=datetime.now()
            )
            await self.cache.set(cache_key, stock_price.model_dump(), self.cache_ttl)
            logger.info(f"Price cached for {ticker}: {price} from {source} (TTL: {self.cache_ttl}s)")
            return stock_price
        
        logger.warning(f"Unable to fetch price for ticker: {ticker}")
        return None