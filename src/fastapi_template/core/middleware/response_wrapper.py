import json

from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse

from fastapi_template.core.model.common_response import BizResponse


async def ResponseWrapperMiddleware(request: Request, call_next):
    if request.url.path.startswith(("/docs", "/redoc", "/openapi")):
        return await call_next(request)  # 문서 관련 경로는 건너뜀

    response = await call_next(request)

    # 스트리밍 응답은 감싸지 않음
    if isinstance(response, StreamingResponse):
        return response

    # content-type이 application/json이 아닐 경우 pass
    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type:
        return response

    # body 읽기
    original_body = b""
    async for chunk in response.body_iterator:
        original_body += chunk

    try:
        parsed_body = json.loads(original_body)
    except Exception:
        parsed_body = original_body.decode("utf-8")

    wrapped = BizResponse.with_status(
        status=response.status_code,
        message="성공" if response.status_code < 400 else "실패",
        data=parsed_body,
    )

    return JSONResponse(
        status_code=response.status_code,
        content=wrapped.model_dump()
    )
