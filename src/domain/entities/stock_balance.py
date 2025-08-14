from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class StockBalance(BaseModel):
    id: Optional[str] = None
    user_id: str
    ticker: str
    quantity: Decimal
    average_price: Decimal
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None