from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from src.application.services.balance_service import BalanceService
from src.application.services.price_service import PriceService
from src.domain.entities.trade import Trade, TradeType
from src.domain.entities.stock_balance import StockBalance
from src.domain.repositories.stock_balance_repository import StockBalanceRepository
from src.domain.repositories.trade_repository import TradeRepository


class TradeService:
    def __init__(
        self,
        trade_repository: TradeRepository,
        stock_balance_repository: StockBalanceRepository,
        balance_service: BalanceService,
        price_service: PriceService
    ):
        self.trade_repository = trade_repository
        self.stock_balance_repository = stock_balance_repository
        self.balance_service = balance_service
        self.price_service = price_service

    async def execute_trade(
        self,
        user_id: str,
        ticker: str,
        trade_type: TradeType,
        quantity: Decimal,
        price: Decimal
    ) -> Trade:
        current_price_data = await self.price_service.get_current_price(ticker)
        if not current_price_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to get current price for ticker"
            )

        current_price = current_price_data.price

        if trade_type == TradeType.BUY and price < current_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Buy price must be >= current market price ({current_price})"
            )

        if trade_type == TradeType.SELL and price > current_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sell price must be <= current market price ({current_price})"
            )

        total_amount = quantity * price

        if trade_type == TradeType.BUY:
            await self._execute_buy(user_id, ticker, quantity, price, total_amount)
        else:
            await self._execute_sell(user_id, ticker, quantity, price, total_amount)

        trade = Trade(
            user_id=user_id,
            ticker=ticker,
            trade_type=trade_type,
            quantity=quantity,
            price=price,
            total_amount=total_amount,
            created_at=datetime.now()
        )

        return await self.trade_repository.create(trade)

    async def _execute_buy(self, user_id: str, ticker: str, quantity: Decimal, price: Decimal, total_amount: Decimal):
        balance = await self.balance_service.get_balance(user_id)
        if not balance or balance.cash_balance < total_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient funds"
            )

        await self.balance_service.update_balance(user_id, -total_amount)

        existing_stock = await self.stock_balance_repository.find_by_user_id_and_ticker(user_id, ticker)
        if existing_stock:
            new_quantity = existing_stock.quantity + quantity
            new_average_price = ((existing_stock.quantity * existing_stock.average_price) + (quantity * price)) / new_quantity
            existing_stock.quantity = new_quantity
            existing_stock.average_price = new_average_price
            existing_stock.current_price = price
            existing_stock.updated_at = datetime.now()
            await self.stock_balance_repository.update(existing_stock)
        else:
            new_stock = StockBalance(
                user_id=user_id,
                ticker=ticker,
                quantity=quantity,
                average_price=price,
                current_price=price,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            await self.stock_balance_repository.create(new_stock)

    async def _execute_sell(self, user_id: str, ticker: str, quantity: Decimal, price: Decimal, total_amount: Decimal):
        existing_stock = await self.stock_balance_repository.find_by_user_id_and_ticker(user_id, ticker)
        if not existing_stock or existing_stock.quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock quantity"
            )

        await self.balance_service.update_balance(user_id, total_amount)

        existing_stock.quantity -= quantity
        existing_stock.current_price = price

        if existing_stock.quantity == 0:
            await self.stock_balance_repository.delete(existing_stock.id)
        else:
            await self.stock_balance_repository.update(existing_stock)