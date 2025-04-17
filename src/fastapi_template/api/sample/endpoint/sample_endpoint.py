from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter

from fastapi_template.api.sample.model.sample_request import SampleRequest
from fastapi_template.api.sample.model.sample_response import SampleResponse

router = APIRouter(
    prefix="/api/v1/user",  # URL prefix
    tags=["Sample"]  # Swagger 문서에서 그룹명
)


@router.post("/register"
    , response_model=SampleResponse
    , summary="Register a new user"
    , description="Register a new user with the provided name and email.")
def register_user(request: SampleRequest):
    return SampleResponse(
        message=f"{request.name}님 등록이 완료되었습니다.",
        data=request,
        timestamp=datetime.now(ZoneInfo("Asia/Seoul"))
    )
