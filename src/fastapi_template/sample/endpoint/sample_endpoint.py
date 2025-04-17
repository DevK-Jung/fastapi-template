from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter

from fastapi_template.sample.model.sample_request import SampleRequest
from fastapi_template.sample.model.sample_response import SampleResponse

router = APIRouter(
    prefix="/user",  # URL prefix
    tags=["User"]  # Swagger 문서에서 그룹명
)


@router.post("/register", response_model=SampleResponse)
def register_user(request: SampleRequest):
    return SampleResponse(
        message=f"{request.name}님 등록이 완료되었습니다.",
        data=request,
        timestamp=datetime.now(ZoneInfo("Asia/Seoul"))
    )
