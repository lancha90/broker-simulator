import logging
from typing import Optional
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.config.database import supabase


class SupabaseUserRepository(UserRepository):
    def __init__(self):
        self.table_name = "ibkr_users"

    async def find_by_api_key(self, api_key: str) -> Optional[User]:
        try:
            response = (supabase.table(self.table_name).select("*").eq("api_key", api_key).execute())
            if response.data:
                return User(**response.data[0])
            return None
        except Exception as e:
            logging.error(f"Error finding user by API key: {e}")
            return None

    async def create(self, user: User) -> User:
        user_dict = user.model_dump(exclude={"id"})
        # Convert datetime to ISO string for JSON serialization
        for field in ["created_at", "updated_at"]:
            if field in user_dict and user_dict[field] is not None:
                user_dict[field] = user_dict[field].isoformat()
        response = supabase.table(self.table_name).insert(user_dict).execute()
        return User(**response.data[0])

    async def find_by_id(self, user_id: str) -> Optional[User]:
        try:
            response = supabase.table(self.table_name).select("*").eq("id", user_id).execute()
            if response.data:
                return User(**response.data[0])
            return None
        except Exception as e:
            logging.error(f"Error finding user by ID: {e}")
            return None