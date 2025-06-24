# 요청 응답 객체 DTO 개념
from typing import Literal, Union

from pydantic import BaseModel, Field, EmailStr


class FilterParams(BaseModel):
    model_config = {
        "extra": "forbid"  # 추가적인 파라미터 방지를 위한 옵션
    }

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


class Sample(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class SampleJsonExample1(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


class SampleJsonExample2(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])


class SampleUserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class SampleUserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5

class FormData(BaseModel):
    username: str
    password: str