from typing import Optional
from pydantic import BaseModel, Field, constr, EmailStr


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