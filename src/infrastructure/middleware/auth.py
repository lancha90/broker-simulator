from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.domain.entities.user import User
from src.infrastructure.adapters.persistence.supabase_user_repository import SupabaseUserRepository


class AuthMiddleware:
    def __init__(self):
        self.user_repository = SupabaseUserRepository()
        self.bearer = HTTPBearer()

    async def authenticate(self, request: Request) -> User:
        try:
            authorization = request.headers.get("Authorization")
            if not authorization:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header missing"
                )

            if not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header format"
                )

            api_key = authorization.replace("Bearer ", "")
            user = await self.user_repository.find_by_api_key(api_key)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid API key"
                )

            return user
            
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )