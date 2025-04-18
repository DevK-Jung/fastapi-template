from typing import Generic, Optional, TypeVar, Any

from pydantic import BaseModel, Field

T = TypeVar("T")


# 공통 응답 처리
class BizResponse(BaseModel, Generic[T]):
    statusCode: str = Field(
        ...,
        description="HTTP 상태 코드",
        json_schema_extra={"example": "OK"}
    )
    resultCode: int = Field(
        ...,
        description="응답 코드",
        json_schema_extra={"example": 200}
    )
    message: str = Field(
        ...,
        description="메시지",
        json_schema_extra={"example": "홍길동님 등록이 완료되었습니다."}
    )
    body: Optional[T] = Field(
        None,
        description="응답 데이터",
        json_schema_extra={"example": {"id": 1, "name": "홍길동"}}
    )
    requestId: Optional[str] = Field(
        None,
        description="요청 ID",
        json_schema_extra={"example": "b3d8e1f4-1234-5678-9abc-def012345678"}
    )

    # timestamp: datetime = Field(
    #     default_factory=lambda: datetime.now(ZoneInfo("Asia/Seoul")),
    #     description="응답 시각",
    #     json_schema_extra={"example": "2025-04-18T14:35:00+09:00"}
    # )

    @classmethod
    def with_status(cls, status: int, message: str, data: Any = None) -> "BizResponse":
        return cls(
            statusCode="OK" if status < 400 else "ERROR",
            resultCode=status,
            message=message,
            body=data,
            requestId=None,
            # timestamp=datetime.now(ZoneInfo("Asia/Seoul"))
        )
