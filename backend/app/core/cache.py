"""Redis async client and cache helpers."""

from typing import Any

import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
    max_connections=20,
)


async def get_redis() -> redis.Redis:  # type: ignore[type-arg]
    """FastAPI dependency for Redis client."""
    return redis_client


class CacheKeyBuilder:
    """Standardized cache key construction."""

    @staticmethod
    def session(jti: str) -> str:
        return f"session:{jti}"

    @staticmethod
    def otp(user_id: str) -> str:
        return f"otp:{user_id}"

    @staticmethod
    def rate_limit(tier: str, scope: str) -> str:
        return f"rl:{tier}:{scope}"

    @staticmethod
    def cache(school_id: str, resource: str, resource_id: str = "") -> str:
        if resource_id:
            return f"cache:{school_id}:{resource}:{resource_id}"
        return f"cache:{school_id}:{resource}"

    @staticmethod
    def idempotency(school_id: str, key: str) -> str:
        return f"idem:{school_id}:{key}"
