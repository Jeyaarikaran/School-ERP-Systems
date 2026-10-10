"""Access log middleware — structured request/response logging."""

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
import structlog

logger = structlog.get_logger()


class AccessLogMiddleware(BaseHTTPMiddleware):
    """Log every HTTP request with method, path, status, and duration."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.monotonic()

        response = await call_next(request)

        duration_ms = round((time.monotonic() - start_time) * 1000, 2)

        # Skip health check noise
        if request.url.path in ("/health", "/ready"):
            return response

        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent", "")[:200],
        )

        return response
