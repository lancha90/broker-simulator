import httpx
from decimal import Decimal
from typing import Optional
from src.application.ports.price_provider import PriceProvider
from src.infrastructure.config.settings import settings


class AlphavantageProvider(PriceProvider):
    def __init__(self):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = settings.alphavantage_api_key

    async def get_price(self, ticker: str) -> Optional[Decimal]:
        try:
            if not self.api_key:
                return None
                
            async with httpx.AsyncClient() as client:
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": ticker,
                    "apikey": self.api_key
                }
                response = await client.get(self.base_url, params=params, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                price = data.get("Global Quote", {}).get("05. price")
                
                if price is not None:
                    return Decimal(str(price))
                return None
        except Exception:
            return None