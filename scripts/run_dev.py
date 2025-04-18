import os
import uvicorn

os.environ["FASTAPI_ENV"] = ".env.dev"

def main():
    os.environ["FASTAPI_ENV"] = ".env.dev"
    uvicorn.run("fastapi_template.main:app", host="127.0.0.1", port=8000, reload=True)