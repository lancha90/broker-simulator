from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    email: str
    api_key: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None