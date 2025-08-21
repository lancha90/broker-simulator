from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from src.application.services.balance_service import BalanceService
from src.domain.entities.user import User
from src.infrastructure.adapters.persistence.supabase_balance_repository import SupabaseBalanceRepository
from src.infrastructure.middleware.auth import AuthMiddleware
from src.infrastructure.config.logging_config import get_logger

logger = get_logger(__name__)


class BalanceResponse(BaseModel):
    user_id: str
    cash_balance: float


router = APIRouter()
auth_middleware = AuthMiddleware()


def get_balance_service():
    return BalanceService(SupabaseBalanceRepository())


@router.get("/v1/balance", response_model=BalanceResponse)
async def get_balance(
    request: Request,
    balance_service: BalanceService = Depends(get_balance_service)
):
    user = await auth_middleware.authenticate(request)
    logger.info(f"Getting balance for user: {user.id}")
    
    balance = await balance_service.get_balance(user.id)
    if not balance:
        logger.info(f"Creating new balance for user: {user.id}")
        balance = await balance_service.create_balance(user.id)
    
    response = BalanceResponse(
        user_id=balance.user_id,
        cash_balance=float(balance.cash_balance)
    )
    
    logger.info(f"Balance response for user {user.id}: cash_balance={response.cash_balance}")
    return response