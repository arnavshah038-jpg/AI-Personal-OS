import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        logger.info(
            f"[{request_id}] Incoming Request | "
            f"{request.method} {request.url.path}"
        )

        request.state.request_id = request_id

        response = await call_next(request)

        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = request_id

        logger.info(
            f"[{request_id}] Completed | "
            f"{request.method} {request.url.path} | "
            f"Status {response.status_code} | "
            f"{process_time:.3f}s"
        )

        return response