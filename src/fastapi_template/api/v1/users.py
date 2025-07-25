from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from fastapi_template.domains.user.dependencies import UserServiceDep
from fastapi_template.domains.user.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
    UserFilter
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def create_user(
        user_data: UserCreate,
        service: UserServiceDep
) -> UserResponse:
    return await service.create_user(user_data)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID"
)
async def get_user(
        user_id: UUID,
        service: UserServiceDep
) -> UserResponse:
    return await service.get_user_by_id(user_id)


@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get users list with filters"
)
async def get_users(
        filters: Annotated[UserFilter, Depends()],
        service: UserServiceDep
) -> UserListResponse:
    return await service.get_users(filters)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user"
)
async def update_user(
        user_id: UUID,
        user_data: UserUpdate,
        service: UserServiceDep
) -> UserResponse:
    return await service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user"
)
async def delete_user(
        user_id: UUID,
        service: UserServiceDep
) -> None:
    await service.delete_user(user_id)
