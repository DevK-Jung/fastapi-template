import os
import uvicorn

os.environ["FASTAPI_ENV"] = ".env.local"

def main():
    os.environ["FASTAPI_ENV"] = ".env.local"  # 환경 파일 설정
    uvicorn.run("fastapi_template.main:app", host="127.0.0.1", port=8000, reload=True)
