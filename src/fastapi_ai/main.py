from fastapi import FastAPI

from fastapi_ai.api.v1 import routers as v1_routers

app = FastAPI(
    title="FastAPI AI API",
    description="LLM 및 Embedding 모델을 활용한 AI 기능 제공 API",
    version="1.0.0",
    contact={
        "name": "김정현",
        "email": "dev.kjung@gmail.com"
    },
)

for router in v1_routers:
    app.include_router(router, prefix="/api/v1")
