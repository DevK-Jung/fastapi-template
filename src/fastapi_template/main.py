from fastapi import FastAPI

from fastapi_template.api.sample.endpoint import sample_endpoint
from fastapi_template.core.config.swagger_config import get_swagger_config

app = FastAPI(**get_swagger_config())

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

app.include_router(sample_endpoint.router)