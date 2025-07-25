from typing import Annotated

from fastapi import Depends

from fastapi_template.core.config.database import DbDep
from fastapi_template.domains.user.repository import UserRepository
from fastapi_template.domains.user.service import UserService


def get_user_repository(session: DbDep) -> UserRepository:
    return UserRepository(session)


def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    return UserService(user_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
