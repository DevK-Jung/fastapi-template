import uuid

from fastapi import Request
from fastapi.logger import logger
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response


# 요청  ID 생성
async def request_id_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    if request.url.path.startswith(("/docs", "/redoc", "/openapi")):
        return await call_next(request)  # 문서 관련 경로는 패스
    # UUID 생성
    request_id = str(uuid.uuid4())

    # 요청 정보 로깅
    logger.info(f"[{request_id}] {request.method} {request.url.path}")

    # request state 에 저장
    request.state.request_id = request_id

    # 응답 객체 가져오기
    response = await call_next(request)

    # 응답 헤더에 삽입
    response.headers["X-Request-ID"] = request_id

    return response
