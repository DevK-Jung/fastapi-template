import uvicorn
from fastapi import FastAPI

from fastapi_ai.api.v1 import routers as v1_routers
from fastapi_ai.core.config.settings import get_settings
from fastapi_ai.core.exception.global_exception_handler import register_global_exception_handlers

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="LLM 및 Embedding 모델을 활용한 AI 기능 제공 API",
    version="1.0.0",
    contact={
        "name": "김정현",
        "email": "dev.kjung@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

register_global_exception_handlers(app)


@app.get("/env")
def read_env():
    return settings.model_dump()


for router in v1_routers:
    app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("fastapi_ai.main:app",
                host=settings.host,
                port=settings.port,
                reload=True)
