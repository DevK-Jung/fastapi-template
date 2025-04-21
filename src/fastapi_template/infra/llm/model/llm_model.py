from pydantic import BaseModel, Field


class AIChunkModel(BaseModel):
    content: str = Field(..., description="생성된 메시지 콘텐츠")
    id: str = Field(..., description="고유 ID (예: run-UUID)")
