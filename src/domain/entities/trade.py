from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class TradeType(str, Enum):
    BUY = "buy"
    SELL = "sell"


class Trade(BaseModel):
    id: Optional[str] = None
    user_id: str
    ticker: str
    trade_type: TradeType
    quantity: Decimal
    price: Decimal
    total_amount: Decimal
    created_at: Optional[datetime] = None