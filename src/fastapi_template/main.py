from fastapi import FastAPI

from fastapi_template.api.sample.endpoint import sample_endpoint
from fastapi_template.core.config.swagger_config import get_swagger_config
from fastapi_template.core.exception.exception_handler import register_exception_handlers
from fastapi_template.core.middleware.request_id_middleware import request_id_middleware
from fastapi_template.core.middleware.response_wrapper import response_wrapper_middleware

app = FastAPI(**get_swagger_config())

# 에러 핸들러 등록
register_exception_handlers(app)

# 미들웨어 등록
app.middleware("http")(response_wrapper_middleware)
app.middleware("http")(request_id_middleware)


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}


# 라우터 등록
app.include_router(sample_endpoint.router)
