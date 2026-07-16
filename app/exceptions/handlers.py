from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import AIServiceError


async def ai_service_exception_handler(
    request: Request,
    exc: AIServiceError,
):
    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error": exc.message,
        },
    )