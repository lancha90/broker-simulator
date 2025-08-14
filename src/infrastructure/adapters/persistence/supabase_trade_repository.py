from typing import List
from src.domain.entities.trade import Trade
from src.domain.repositories.trade_repository import TradeRepository
from src.infrastructure.config.database import supabase


class SupabaseTradeRepository(TradeRepository):
    def __init__(self):
        self.table_name = "ibkr_trades"

    async def create(self, trade: Trade) -> Trade:
        trade_dict = trade.model_dump(exclude={"id"})
        response = supabase.table(self.table_name).insert(trade_dict).execute()
        return Trade(**response.data[0])

    async def find_by_user_id(self, user_id: str) -> List[Trade]:
        try:
            response = supabase.table(self.table_name).select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            return [Trade(**item) for item in response.data]
        except Exception:
            return []