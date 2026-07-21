from fastapi import FastAPI

from app.api.routes import router
from app.api.memory_routes import router as memory_router
from app.api.dashboard import router as dashboard_router

from app.exceptions.custom_exceptions import AIServiceError
from app.exceptions.handlers import ai_service_exception_handler

from app.middleware.logging_middleware import LoggingMiddleware


app = FastAPI(
    title="AI Personal OS",
    version="1.0.0",
    description=(
        "Production-ready AI Personal Assistant "
        "with Memory, RAG, Qdrant and LLM capabilities"
    ),
)


# ==========================
# Middleware
# ==========================

app.add_middleware(
    LoggingMiddleware
)


# ==========================
# Exception Handlers
# ==========================

app.add_exception_handler(
    AIServiceError,
    ai_service_exception_handler,
)


# ==========================
# API Routes
# ==========================

app.include_router(
    router
)

app.include_router(
    memory_router
)

app.include_router(
    dashboard_router
)


# ==========================
# Health Check
# ==========================

@app.get("/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "service": "AI Personal OS",
        "version": "1.0.0"
    }