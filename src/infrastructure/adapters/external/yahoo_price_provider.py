import httpx
from decimal import Decimal
from typing import Optional
from src.application.ports.price_provider import PriceProvider


class YahooPriceProvider(PriceProvider):
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"

    async def get_price(self, ticker: str) -> Optional[Decimal]:
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/{ticker}?interval=1d&range=1d"
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                price = data.get("chart", {}).get("result", [{}])[0].get("meta", {}).get("regularMarketPrice")
                
                if price is not None:
                    return Decimal(str(price))
                return None
        except Exception:
            return None