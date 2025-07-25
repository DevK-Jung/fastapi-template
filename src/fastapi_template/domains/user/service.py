from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from passlib.context import CryptContext

from fastapi_template.domains.user.models import User
from fastapi_template.domains.user.repository import UserRepository
from fastapi_template.domains.user.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
    UserFilter
)


class UserService:
    def __init__(self, user_repository: UserRepository):  # Repository 주입
        self.repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        existing_username = await self.repository.get_by_username(user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        hashed_password = self._hash_password(user_data.password)
        user = await self.repository.create(user_data, hashed_password)
        return UserResponse.model_validate(user)

    async def get_user_by_id(self, user_id: UUID) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = await self.repository.get_by_email(email)
        if not user:
            return None
        return UserResponse.model_validate(user)

    async def get_users(self, filters: UserFilter) -> UserListResponse:
        users, total = await self.repository.get_list(filters)
        user_responses = [UserResponse.model_validate(user) for user in users]

        return UserListResponse(
            users=user_responses,
            total=total,
            page=filters.page,
            size=filters.size
        )

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserResponse:
        if user_data.email:
            existing_user = await self.repository.get_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        if user_data.username:
            existing_username = await self.repository.get_by_username(user_data.username)
            if existing_username and existing_username.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )

        user = await self.repository.update(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: UUID) -> bool:
        success = await self.repository.delete(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return True

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.repository.get_by_email(email)
        if not user or not self._verify_password(password, user.hashed_password):
            return None
        return user
