from typing import Optional
from src.domain.entities.balance import Balance
from src.domain.repositories.balance_repository import BalanceRepository
from src.infrastructure.config.database import supabase


class SupabaseBalanceRepository(BalanceRepository):
    def __init__(self):
        self.table_name = "ibkr_balances"

    async def find_by_user_id(self, user_id: str) -> Optional[Balance]:
        try:
            response = supabase.table(self.table_name).select("*").eq("user_id", user_id).execute()
            if response.data:
                return Balance(**response.data[0])
            return None
        except Exception:
            return None

    async def create(self, balance: Balance) -> Balance:
        balance_dict = balance.model_dump(exclude={"id"})
        # Convert Decimal to float for JSON serialization
        if "cash_balance" in balance_dict:
            balance_dict["cash_balance"] = float(balance_dict["cash_balance"])
        response = supabase.table(self.table_name).insert(balance_dict).execute()
        return Balance(**response.data[0])

    async def update(self, balance: Balance) -> Balance:
        balance_dict = balance.model_dump(exclude={"id", "created_at"})
        # Convert Decimal to float for JSON serialization
        if "cash_balance" in balance_dict:
            balance_dict["cash_balance"] = float(balance_dict["cash_balance"])
        response = supabase.table(self.table_name).update(balance_dict).eq("id", balance.id).execute()
        return Balance(**response.data[0])