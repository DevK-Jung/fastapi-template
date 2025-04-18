from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, EmailStr, constr


class SampleRequest(BaseModel):
    name: constr(min_length=2) = Field(
        ...,
        title="이름",
        description="사용자의 이름",
        json_schema_extra={"example": "홍길동"}
    )
    age: int = Field(
        ...,
        ge=0,
        le=120,
        title="나이",
        description="사용자의 나이",
        json_schema_extra={"example": 30}
    )
    email: EmailStr = Field(
        ...,
        title="이메일",
        description="사용자의 이메일 주소",
        json_schema_extra={"example": "hong@example.com"}
    )
    phone: Optional[str] = Field(
        default=None,
        title="전화번호",
        description="사용자의 전화번호",
        json_schema_extra={"example": "010-1234-5678"}
    )
    address: Optional[str] = Field(
        default=None,
        title="주소",
        description="사용자의 상세 주소",
        json_schema_extra={"example": "서울특별시 강남구"}
    )
    city: Optional[str] = Field(
        default=None,
        title="도시",
        description="사용자가 거주하는 도시",
        json_schema_extra={"example": "서울"}
    )
    state: Optional[str] = Field(
        default=None,
        title="시/도",
        description="사용자가 거주하는 시/도",
        json_schema_extra={"example": "서울특별시"}
    )
    country: Optional[str] = Field(
        default=None,
        title="국가",
        description="사용자가 거주하는 국가",
        json_schema_extra={"example": "대한민국"}
    )
    zip_code: Optional[str] = Field(
        default=None,
        title="우편번호",
        description="사용자의 우편번호",
        json_schema_extra={"example": "12345"}
    )
    latitude: Optional[float] = Field(
        default=None,
        title="위도",
        description="주소의 위도 정보",
        json_schema_extra={"example": 37.5665}
    )
    longitude: Optional[float] = Field(
        default=None,
        title="경도",
        description="주소의 경도 정보",
        json_schema_extra={"example": 126.9780}
    )


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
