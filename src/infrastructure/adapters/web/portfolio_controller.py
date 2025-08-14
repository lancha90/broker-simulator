from typing import List
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.application.services.portfolio_service import PortfolioService
from src.infrastructure.adapters.persistence.supabase_stock_balance_repository import SupabaseStockBalanceRepository
from src.infrastructure.middleware.auth import AuthMiddleware


class StockHolding(BaseModel):
    ticker: str
    quantity: float
    average_price: float


class PortfolioResponse(BaseModel):
    user_id: str
    holdings: List[StockHolding]


router = APIRouter()
auth_middleware = AuthMiddleware()


def get_portfolio_service():
    return PortfolioService(SupabaseStockBalanceRepository())


@router.get("/v1/portfolio", response_model=PortfolioResponse)
async def get_portfolio(
    request: Request,
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    user = await auth_middleware.authenticate(request)
    
    stock_balances = await portfolio_service.get_portfolio(user.id)
    
    holdings = [
        StockHolding(
            ticker=sb.ticker,
            quantity=float(sb.quantity),
            average_price=float(sb.average_price)
        )
        for sb in stock_balances
    ]
    
    return PortfolioResponse(
        user_id=user.id,
        holdings=holdings
    )