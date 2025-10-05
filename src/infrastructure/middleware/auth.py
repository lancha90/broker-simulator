from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.domain.entities.user import User
from src.infrastructure.adapters.persistence.postgres import PostgresUserRepository
from src.infrastructure.config.logging_config import get_logger

logger = get_logger(__name__)


class AuthMiddleware:
    def __init__(self):
        self.user_repository = PostgresUserRepository()
        self.bearer = HTTPBearer()

    async def authenticate(self, request: Request) -> User:
        try:
            logger.info(f"Authentication attempt for {request.url.path}" )

            authorization = request.headers.get("Authorization")
            if not authorization:
                logger.warning("Authorization header missing")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header missing"
                )

            if not authorization.startswith("Bearer "):
                logger.warning("Invalid authorization header format")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header format"
                )

            api_key = authorization.replace("Bearer ", "")
            logger.info(f"Looking up user with API key: {api_key[:4]}***")
            
            user = await self.user_repository.find_by_api_key(api_key)
            
            if not user:
                logger.warning(f"Invalid API key attempted: {api_key[:4]}***")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid API key"
                )

            logger.info(f"User authenticated successfully: {user.id} ({user.email})")
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )