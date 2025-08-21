from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from src.application.services.price_service import PriceService
from src.infrastructure.adapters.external.composite_price_provider import CompositePriceProvider
from src.infrastructure.adapters.external.memory_cache import MemoryCache
from src.infrastructure.middleware.auth import AuthMiddleware
from src.infrastructure.config.logging_config import get_logger

logger = get_logger(__name__)


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
    user = await auth_middleware.authenticate(request)
    logger.info(f"Price request from user {user.id} for ticker: {ticker}")
    
    stock_price = await price_service.get_current_price(ticker.upper())
    if not stock_price:
        logger.warning(f"Price not found for ticker {ticker} requested by user {user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Price not found for ticker: {ticker}"
        )
    
    response = PriceResponse(
        ticker=stock_price.ticker,
        price=float(stock_price.price),
        source=stock_price.source,
        timestamp=stock_price.timestamp.isoformat()
    )
    
    logger.info(f"Price response for user {user.id}: {ticker}=${response.price} (source: {response.source})")
    return response