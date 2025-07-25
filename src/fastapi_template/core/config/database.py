from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel

from fastapi_template.core.config.settings import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def setup_database():
    """데이터베이스 초기화"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def cleanup_database():
    """데이터베이스 정리"""
    await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


DbDep = Annotated[AsyncSession, Depends(get_db)]
