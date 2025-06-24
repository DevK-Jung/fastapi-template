# 요청 응답 객체 DTO 개념
from typing import Literal, Union

from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # 추가적인 파라미터 방지를 위한 옵션

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


class Sample(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
