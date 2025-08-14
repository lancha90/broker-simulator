from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from src.application.services.price_service import PriceService
from src.infrastructure.adapters.external.composite_price_provider import CompositePriceProvider
from src.infrastructure.adapters.external.memory_cache import MemoryCache
from src.infrastructure.middleware.auth import AuthMiddleware


class PriceResponse(BaseModel):
    ticker: str
    price: float
    source: str
    timestamp: str


router = APIRouter()
auth_middleware = AuthMiddleware()
cache = MemoryCache()


def get_price_service():
    return PriceService(CompositePriceProvider(), cache)


@router.get("/v1/price/{ticker}", response_model=PriceResponse)
async def get_price(
    ticker: str,
    request: Request,
    price_service: PriceService = Depends(get_price_service)
):
    await auth_middleware.authenticate(request)
    
    stock_price = await price_service.get_current_price(ticker.upper())
    if not stock_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Price not found for ticker: {ticker}"
        )
    
    return PriceResponse(
        ticker=stock_price.ticker,
        price=float(stock_price.price),
        source=stock_price.source,
        timestamp=stock_price.timestamp.isoformat()
    )