from fastapi import Request, HTTPException, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi_template.core.exception.model.error_model import ErrorResponseModel


def register_exception_handlers(app: FastAPI):
    # default 에러 처리
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        error_response = ErrorResponseModel(
            statusCode=500,
            resultCode="INTERNAL_SERVER_ERROR",
            message=str(exc),
            path=str(request.url),
            traceId=None
        )

        return JSONResponse(
            status_code=500,
            content=error_response.model_dump(),
        )

    # 라우트 외부 처리(경로 매핑이 안된 경우, HTTP Method가 잘못된 경우 등)
    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        error_response = ErrorResponseModel(
            statusCode=exc.status_code,
            resultCode="NOT_FOUND" if exc.status_code == 404 else "HTTP_EXCEPTION",
            message=exc.detail,
            path=str(request.url),
            traceId=None
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )

    # fastAPI HttpException 처리
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        error_response = ErrorResponseModel(
            statusCode=exc.status_code,
            resultCode="HTTP_EXCEPTION",
            message=exc.detail,
            path=str(request.url),
            traceId=None
        )

        return JSONResponse(status_code=exc.status_code,
                            content=error_response.model_dump())

    # 요청 파라미터 Validation
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        error_details = [
            {
                "field": ".".join(str(loc) for loc in err["loc"]),
                "message": err["msg"],
                "type": err["type"]
            }
            for err in exc.errors()
        ]

        error_response = ErrorResponseModel(
            statusCode=422,
            resultCode="REQUEST_VALIDATION_ERROR",
            message="입력값 검증에 실패했습니다.",
            path=str(request.url),
            traceId=None  # 필요시 request header에서 추출 가능
        )

        return JSONResponse(
            status_code=422,
            content={
                **error_response.model_dump(),
                "errors": error_details  # 필드별 상세 오류 정보 포함
            }
        )
