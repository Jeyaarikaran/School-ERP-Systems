"""Rate limiting middleware using Redis."""

import time
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from app.core.config import settings
from app.core.cache import redis_client

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Token bucket rate limiter.
    Limits by IP if unauthenticated, or by user ID if authenticated.
    """
    def __init__(self, app: ASGIApp, requests_per_minute: int = 600) -> None:
        super().__init__(app)
        self.limit = requests_per_minute

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Pass-through if redis is not configured
        if not settings.redis_url:
            return await call_next(request)

        # Identify client (simple heuristic for middleware)
        client_id = request.client.host if request.client else "unknown"
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # In a real app, we'd decode the JWT. For middleware speed, 
            # we might just use the token signature as the key if we don't want to decode it,
            # but ideally this happens after AuthMiddleware.
            client_id = auth_header.split(".")[-1]
            
        key = f"rate_limit:{client_id}"
        current_minute = int(time.time() / 60)
        redis_key = f"{key}:{current_minute}"
        
        try:
            count = await redis_client.incr(redis_key)
            if count == 1:
                await redis_client.expire(redis_key, 60)
                
            if count > self.limit:
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded. Try again in a minute."},
                    headers={"Retry-After": "60"}
                )
                
        except Exception:
            # Fail open if Redis is down
            pass

        return await call_next(request)
