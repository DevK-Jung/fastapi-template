from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)
    full_name: str | None = Field(default=None, max_length=100)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=3, max_length=50)
    full_name: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    full_name: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    size: int


class UserFilter(BaseModel):
    email: str | None = None
    username: str | None = None
    is_active: str | None = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)
