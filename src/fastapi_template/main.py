from fastapi import FastAPI

from src.fastapi_template.sample.endpoint import sample_endpoint

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

app.include_router(sample_endpoint.router)