from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel, Field, constr

from fastapi_template.api.sample.model.sample_model import SampleRequest, SampleResponse

router = APIRouter(
    prefix="/api/v1/sample",  # URL prefix
    tags=["Sample"]  # Swagger 문서에서 그룹명
)


@router.post("/user/register"
    , response_model=SampleResponse
    , summary="Register a new user"
    , description="Register a new user with the provided name and email.")
def register_user(request: SampleRequest):
    return SampleResponse(
        message=f"{request.name}님 등록이 완료되었습니다.",
        data=request,
        # timestamp=datetime.now(ZoneInfo("Asia/Seoul"))
    )


@router.get("/exception")
def exception():
    raise Exception("에러 발생")


@router.get("/http-exception")
def http_exception():
    raise HTTPException(400, "Bad Request")


class ItemRequest(BaseModel):
    name: constr(min_length=2)
    age: Optional[int] = Field(None, title="나이", description="나이")


@router.get("/request-validation-error")
def http_exception(item: ItemRequest = Depends()):
    return item
