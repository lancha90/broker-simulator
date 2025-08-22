import httpx
from decimal import Decimal
from typing import Optional
from src.application.ports.price_provider import PriceProvider
from src.infrastructure.config.logging_config import get_logger

logger = get_logger(__name__)


class YahooPriceProvider(PriceProvider):
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"

    async def get_price(self, ticker: str) -> Optional[Decimal]:
        logger.info(f"Fetching price from Yahoo Finance for {ticker}")
        
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/{ticker}?interval=1d&range=1d"
                logger.debug(f"Making request to Yahoo Finance: {url}")

                response = await client.get(url, timeout=10.0, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()
                logger.debug(f"Yahoo Finance response status: {response.status_code}")
                
                data = response.json()
                price = data.get("chart", {}).get("result", [{}])[0].get("meta", {}).get("regularMarketPrice")
                
                if price is not None:
                    logger.info(f"Yahoo Finance returned price for {ticker}: {price}")
                    return Decimal(str(price))
                else:
                    logger.warning(f"Yahoo Finance returned no price data for {ticker}")
                    return None
        except httpx.HTTPStatusError as e:
            logger.error(f"Yahoo Finance HTTP error for {ticker}: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.TimeoutException:
            logger.error(f"Yahoo Finance timeout for {ticker}")
            return None
        except Exception as e:
            logger.error(f"Yahoo Finance unexpected error for {ticker}: {str(e)}")
            return None