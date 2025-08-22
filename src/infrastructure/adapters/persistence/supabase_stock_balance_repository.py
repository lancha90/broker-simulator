from typing import List, Optional
from src.domain.entities.stock_balance import StockBalance
from src.domain.repositories.stock_balance_repository import StockBalanceRepository
from src.infrastructure.config.database import supabase


class SupabaseStockBalanceRepository(StockBalanceRepository):
    def __init__(self):
        self.table_name = "ibkr_stock_balances"

    async def find_by_user_id(self, user_id: str) -> List[StockBalance]:
        try:
            response = supabase.table(self.table_name).select("*").eq("user_id", user_id).execute()
            return [StockBalance(**item) for item in response.data]
        except Exception:
            return []

    async def find_by_user_id_and_ticker(self, user_id: str, ticker: str) -> Optional[StockBalance]:
        try:
            response = supabase.table(self.table_name).select("*").eq("user_id", user_id).eq("ticker", ticker).execute()
            if response.data:
                return StockBalance(**response.data[0])
            return None
        except Exception:
            return None

    async def create(self, stock_balance: StockBalance) -> StockBalance:
        stock_balance_dict = stock_balance.model_dump(exclude={"id"})
        # Convert Decimal fields to float for JSON serialization
        if "quantity" in stock_balance_dict:
            stock_balance_dict["quantity"] = float(stock_balance_dict["quantity"])
        if "average_price" in stock_balance_dict:
            stock_balance_dict["average_price"] = float(stock_balance_dict["average_price"])
        # Convert datetime to ISO string for JSON serialization
        for field in ["created_at", "updated_at"]:
            if field in stock_balance_dict and stock_balance_dict[field] is not None:
                stock_balance_dict[field] = stock_balance_dict[field].isoformat()
        response = supabase.table(self.table_name).insert(stock_balance_dict).execute()
        return StockBalance(**response.data[0])

    async def update(self, stock_balance: StockBalance) -> StockBalance:
        stock_balance_dict = stock_balance.model_dump(exclude={"id", "created_at"})
        # Convert Decimal fields to float for JSON serialization
        if "quantity" in stock_balance_dict:
            stock_balance_dict["quantity"] = float(stock_balance_dict["quantity"])
        if "average_price" in stock_balance_dict:
            stock_balance_dict["average_price"] = float(stock_balance_dict["average_price"])
        # Convert datetime to ISO string for JSON serialization
        for field in ["updated_at"]:
            if field in stock_balance_dict and stock_balance_dict[field] is not None:
                stock_balance_dict[field] = stock_balance_dict[field].isoformat()
        response = supabase.table(self.table_name).update(stock_balance_dict).eq("id", stock_balance.id).execute()
        return StockBalance(**response.data[0])

    async def delete(self, stock_balance_id: str) -> None:
        supabase.table(self.table_name).delete().eq("id", stock_balance_id).execute()