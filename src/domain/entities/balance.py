from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class Balance(BaseModel):
    id: Optional[str] = None
    user_id: str
    cash_balance: Decimal
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None