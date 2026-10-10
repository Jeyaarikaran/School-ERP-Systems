"""School ERP Backend — FastAPI Application."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.errors import register_exception_handlers
from app.api.v1.router import api_router
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.access_log import AccessLogMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

import sentry_sdk

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application startup and shutdown lifecycle."""
    setup_logging()
    logger.info("application_startup", env=settings.app_env, version="0.1.0")
    
    if settings.app_env != "development" and hasattr(settings, "sentry_dsn") and settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.app_env,
            traces_sample_rate=0.1,
            profiles_sample_rate=0.1,
        )

    # Startup: initialize connections
    # Database and Redis pools initialized lazily via dependencies

    yield

    # Shutdown: cleanup
    logger.info("application_shutdown")


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title="School ERP API",
        description="Multi-tenant School Management System",
        version="0.1.0",
        docs_url="/docs" if settings.app_debug else None,
        redoc_url="/redoc" if settings.app_debug else None,
        openapi_url="/openapi.json" if settings.app_debug else None,
        lifespan=lifespan,
    )

    # Middleware (order matters: last added = first executed)
    app.add_middleware(RateLimitMiddleware, requests_per_minute=600)
    app.add_middleware(AccessLogMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-Request-ID",
            "Idempotency-Key",
        ],
        expose_headers=[
            "X-Request-ID",
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
            "Retry-After",
        ],
    )

    # Routes
    app.include_router(api_router, prefix="/api/v1")

    # Exception Handlers
    register_exception_handlers(app)

    return app


app = create_app()
