from fastapi import FastAPI

from fastapi_template.api.sample.endpoint import sample_endpoint
from fastapi_template.core.config.swagger_config import get_swagger_config
from fastapi_template.core.exception.exception_handler import register_exception_handlers

app = FastAPI(**get_swagger_config())
register_exception_handlers(app)


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}


app.include_router(sample_endpoint.router)
