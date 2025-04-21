from fastapi_template.core.config.config import get_settings
from fastapi_template.infra.llm.llm_client import LLMClient

settings = get_settings()

class AiService:
    def __init__(self):

        self.llm_client = LLMClient(
            model=settings.ai_model,
            api_base=settings.ai_url,
        )

    async def stream_response(self, prompt: str):
        async for chunk in self.llm_client.chat_stream(prompt=prompt):
            yield chunk.model_dump_json()
