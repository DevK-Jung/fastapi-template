from fastapi import FastAPI

from fastapi_template.api.sample.endpoint import sample_endpoint
from fastapi_template.core.config.swagger_config import get_swagger_config
from fastapi_template.core.exception.exception_handler import register_exception_handlers
from fastapi_template.core.middleware.response_wrapper import ResponseWrapperMiddleware

app = FastAPI(**get_swagger_config())

# 에러 핸들러 등록
register_exception_handlers(app)

# 공통 응답 미들웨어 등록
app.middleware("http")(ResponseWrapperMiddleware)


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}


app.include_router(sample_endpoint.router)
