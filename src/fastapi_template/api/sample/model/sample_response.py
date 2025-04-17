from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field
from datetime import datetime

from fastapi_template.api.sample.model.sample_request import SampleRequest


class SampleResponse(BaseModel):
    message: str = Field(
        ...,
        description="결과 메시지",
        json_schema_extra={"example": "홍길동님 등록이 완료되었습니다."}
    )
    data: SampleRequest = Field(
        ...,
        description="등록된 사용자 데이터 (요청과 동일)",
        json_schema_extra={
            "example": {
                "name": "홍길동",
                "age": 30,
                "email": "hong@example.com",
                "phone": "010-1234-5678",
                "address": "서울특별시 강남구",
                "city": "서울",
                "state": "서울특별시",
                "country": "대한민국",
                "zip_code": "12345",
                "latitude": 37.5665,
                "longitude": 126.978
            }
        }
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("Asia/Seoul")),
        description="응답 시간 (KST)",
        json_schema_extra={"example": "2024-04-17T21:00:00+09:00"}
    )
