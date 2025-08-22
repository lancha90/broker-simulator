from typing import List
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.application.services.portfolio_service import PortfolioService
from src.application.services.balance_service import BalanceService
from src.infrastructure.adapters.persistence.supabase_stock_balance_repository import SupabaseStockBalanceRepository
from src.infrastructure.adapters.persistence.supabase_balance_repository import SupabaseBalanceRepository
from src.infrastructure.middleware.auth import AuthMiddleware
from src.infrastructure.config.logging_config import get_logger

logger = get_logger(__name__)


class StockHolding(BaseModel):
    ticker: str
    quantity: float
    average_price: float


class PortfolioResponse(BaseModel):
    user_id: str
    holdings: List[StockHolding]
    total_invested_value: float
    cash_balance: float


router = APIRouter()
auth_middleware = AuthMiddleware()


def get_portfolio_service():
    return PortfolioService(SupabaseStockBalanceRepository())

def get_balance_service():
    return BalanceService(SupabaseBalanceRepository())


@router.get("/v1/portfolio", response_model=PortfolioResponse)
async def get_portfolio(
    request: Request,
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
    balance_service: BalanceService = Depends(get_balance_service)
):
    user = await auth_middleware.authenticate(request)
    logger.info(f"Portfolio request from user {user.id}")
    
    # Get stock balances
    stock_balances = await portfolio_service.get_portfolio(user.id)
    
    # Calculate total invested value (quantity * average_price for each holding)
    total_invested_value = sum(
        float(sb.quantity) * float(sb.average_price) for sb in stock_balances
    )
    
    # Get user cash balance
    balance = await balance_service.get_balance(user.id)
    cash_balance = float(balance.cash_balance) if balance else 0.0
    
    holdings = [
        StockHolding(
            ticker=sb.ticker,
            quantity=float(sb.quantity),
            average_price=float(sb.average_price)
        )
        for sb in stock_balances
    ]
    
    response = PortfolioResponse(
        user_id=user.id,
        holdings=holdings,
        total_invested_value=total_invested_value,
        cash_balance=cash_balance
    )
    
    logger.info(f"Portfolio response for user {user.id}: {len(holdings)} holdings, invested_value={total_invested_value}, cash_balance={cash_balance}")
    return response