from fastapi import APIRouter
from sse_starlette import EventSourceResponse

from fastapi_template.api.ai.service.ai_service import AiService

router = APIRouter(
    prefix="/api/v1/ai",  # URL prefix
    tags=["AI"]  # Swagger 문서에서 그룹명
)

ai_service = AiService()

@router.get("/stream")
async def stream_chat(prompt: str):
    return EventSourceResponse(ai_service.stream_response(prompt=prompt))
