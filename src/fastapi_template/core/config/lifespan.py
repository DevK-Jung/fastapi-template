from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_template.core.config.database import setup_database, cleanup_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    # 테이블 세팅
    await setup_database()

    yield
    # 리소스 정리
    await cleanup_database()
