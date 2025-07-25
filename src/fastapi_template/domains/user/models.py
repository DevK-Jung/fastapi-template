from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=50)
    full_name: str | None = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
