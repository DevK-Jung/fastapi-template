from typing import Optional

from pydantic import BaseModel, Field


class ErrorResponseModel(BaseModel):
    statusCode: int = Field(
        ...,
        description="HTTP 상태 코드",
        json_schema_extra={"example": 400}
    )
    resultCode: str = Field(
        ...,
        description="내부 정의 에러 코드",
        json_schema_extra={"example": "BAD_REQUEST"}
    )
    message: str = Field(
        ...,
        description="에러 메시지",
        json_schema_extra={"example": "요청이 잘못되었습니다"}
    )
    path: Optional[str] = Field(
        None,
        description="요청 경로",
        json_schema_extra={"example": "/api/v1/users/1"}
    )
    traceId: Optional[str] = Field(
        None,
        description="트래킹 ID",
        json_schema_extra={"example": "b82f3e16-xxxx-yyyy-zzzz"}
    )
