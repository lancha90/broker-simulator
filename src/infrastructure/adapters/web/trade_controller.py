from decimal import Decimal
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.application.services.balance_service import BalanceService
from src.application.services.price_service import PriceService
from src.application.services.trade_service import TradeService
from src.domain.entities.trade import TradeType
from src.infrastructure.adapters.external.composite_price_provider import CompositePriceProvider
from src.infrastructure.adapters.external.memory_cache import MemoryCache
from src.infrastructure.adapters.persistence.supabase_balance_repository import SupabaseBalanceRepository
from src.infrastructure.adapters.persistence.supabase_stock_balance_repository import SupabaseStockBalanceRepository
from src.infrastructure.adapters.persistence.supabase_trade_repository import SupabaseTradeRepository
from src.infrastructure.middleware.auth import AuthMiddleware


class TradeRequest(BaseModel):
    ticker: str
    action: str  # "buy" or "sell"
    quantity: float
    price: float


class TradeResponse(BaseModel):
    id: str
    user_id: str
    ticker: str
    trade_type: str
    quantity: float
    price: float
    total_amount: float
    timestamp: str


router = APIRouter()
auth_middleware = AuthMiddleware()
cache = MemoryCache()


def get_trade_service():
    balance_service = BalanceService(SupabaseBalanceRepository())
    price_service = PriceService(CompositePriceProvider(), cache)
    
    return TradeService(
        SupabaseTradeRepository(),
        SupabaseStockBalanceRepository(),
        balance_service,
        price_service
    )


@router.post("/v1/trade", response_model=TradeResponse)
async def execute_trade(
    trade_request: TradeRequest,
    request: Request,
    trade_service: TradeService = Depends(get_trade_service)
):
    user = await auth_middleware.authenticate(request)
    
    trade_type = TradeType.BUY if trade_request.action.lower() == "buy" else TradeType.SELL
    
    trade = await trade_service.execute_trade(
        user_id=user.id,
        ticker=trade_request.ticker.upper(),
        trade_type=trade_type,
        quantity=Decimal(str(trade_request.quantity)),
        price=Decimal(str(trade_request.price))
    )
    
    return TradeResponse(
        id=trade.id,
        user_id=trade.user_id,
        ticker=trade.ticker,
        trade_type=trade.trade_type.value,
        quantity=float(trade.quantity),
        price=float(trade.price),
        total_amount=float(trade.total_amount),
        timestamp=trade.created_at.isoformat() if trade.created_at else ""
    )