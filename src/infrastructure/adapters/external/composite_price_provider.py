from decimal import Decimal
from typing import List, Optional, Tuple
from src.application.ports.price_provider import PriceProvider
from src.infrastructure.adapters.external.yahoo_price_provider import YahooPriceProvider
from src.infrastructure.adapters.external.alphavantage_price_provider import AlphavantageProvider
from src.infrastructure.config.logging_config import get_logger

logger = get_logger(__name__)


class CompositePriceProvider(PriceProvider):
    def __init__(self):
        self.providers: List[PriceProvider] = [
            YahooPriceProvider(),
            AlphavantageProvider()
        ]

    async def get_price(self, ticker: str) -> Optional[Tuple[Decimal, str]]:
        logger.info(f"Attempting to get price for {ticker} using fallback chain")
        
        for i, provider in enumerate(self.providers):
            provider_name = provider.__class__.__name__
            try:
                logger.info(f"Trying provider {i+1}/{len(self.providers)}: {provider_name} for {ticker}")
                result = await provider.get_price(ticker)
                if result is not None:
                    price, source = result
                    logger.info(f"Price found for {ticker}: {price} (provider: {provider_name}, source: {source})")
                    return result
                else:
                    logger.warning(f"Provider {provider_name} returned None for {ticker}")
            except Exception as e:
                logger.warning(f"Provider {provider_name} failed for {ticker}: {str(e)}")
                continue
        
        logger.error(f"All providers failed to get price for {ticker}")
        return None