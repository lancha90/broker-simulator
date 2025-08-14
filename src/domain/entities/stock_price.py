from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class StockPrice(BaseModel):
    ticker: str
    price: Decimal
    source: str
    timestamp: datetime