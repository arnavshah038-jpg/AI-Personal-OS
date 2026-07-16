from fastapi import FastAPI

from app.api.routes import router
from app.api.memory_routes import router as memory_router
from app.api.dashboard import router as dashboard_router
from app.core.qdrant_client import qdrant
from app.exceptions.custom_exceptions import AIServiceError
from app.exceptions.handlers import ai_service_exception_handler
from app.middleware.logging_middleware import LoggingMiddleware

app = FastAPI(
    title="AI Personal OS",
    version="1.0.0",
    description="Production-ready AI Personal Assistant",
)

# Register Middleware
app.add_middleware(
    LoggingMiddleware
)

# Register Exception Handler
app.add_exception_handler(
    AIServiceError,
    ai_service_exception_handler,
)

# Register Routes
app.include_router(
    router
)

app.include_router(
    memory_router
)

app.include_router(
    dashboard_router
)