from decimal import Decimal
from typing import Optional
from src.domain.entities.balance import Balance
from src.domain.repositories.balance_repository import BalanceRepository


class BalanceService:
    def __init__(self, balance_repository: BalanceRepository):
        self.balance_repository = balance_repository

    async def get_balance(self, user_id: str) -> Optional[Balance]:
        return await self.balance_repository.find_by_user_id(user_id)

    async def create_balance(self, user_id: str, initial_balance: Decimal = Decimal("10000")) -> Balance:
        balance = Balance(
            user_id=user_id,
            cash_balance=initial_balance
        )
        return await self.balance_repository.create(balance)

    async def update_balance(self, user_id: str, amount: Decimal) -> Optional[Balance]:
        balance = await self.balance_repository.find_by_user_id(user_id)
        if not balance:
            return None
        
        balance.cash_balance += amount
        return await self.balance_repository.update(balance)