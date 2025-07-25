from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_template.domains.user.models import User
from fastapi_template.domains.user.schemas import UserCreate, UserUpdate, UserFilter


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_data: UserCreate, hashed_password: str) -> User:
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_list(self, filters: UserFilter) -> tuple[list[User], int]:
        statement = select(User)

        if filters.email:
            statement = statement.where(User.email.contains(filters.email))
        if filters.username:
            statement = statement.where(User.username.contains(filters.username))
        if filters.is_active is not None:
            statement = statement.where(User.is_active.is_(filters.is_active))

        total_statement = select(func.count(User.id)).select_from(statement.subquery())
        total_result = await self.session.execute(total_statement)
        total = total_result.scalar_one()

        offset = (filters.page - 1) * filters.size
        statement = statement.offset(offset).limit(filters.size)

        result = await self.session.execute(statement)
        users = result.scalars().all()

        return users, total

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()
        return True
