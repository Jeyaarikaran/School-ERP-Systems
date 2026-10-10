"""Health and readiness endpoints — no authentication required."""

import time
from typing import Any

import structlog
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.cache import get_redis

logger = structlog.get_logger()
router = APIRouter()

_start_time = time.time()


@router.get("/health")
async def health_check() -> dict[str, Any]:
    """Liveness probe — returns 200 if process is alive."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "uptime_seconds": round(time.time() - _start_time),
    }


@router.get("/ready")
async def readiness_check(
    db: AsyncSession = Depends(get_db_session),
    redis: Any = Depends(get_redis),
) -> dict[str, Any]:
    """Readiness probe — checks DB and Redis connectivity."""
    checks: dict[str, dict[str, Any]] = {}

    # Database check
    try:
        db_start = time.monotonic()
        await db.execute(text("SELECT 1"))
        db_latency = round((time.monotonic() - db_start) * 1000, 1)
        checks["database"] = {"status": "up", "latency_ms": db_latency}
    except Exception as e:
        checks["database"] = {"status": "down", "error": str(e)}
        logger.error("readiness_check_failed", component="database", error=str(e))

    # Redis check
    try:
        redis_start = time.monotonic()
        await redis.ping()
        redis_latency = round((time.monotonic() - redis_start) * 1000, 1)
        checks["redis"] = {"status": "up", "latency_ms": redis_latency}
    except Exception as e:
        checks["redis"] = {"status": "down", "error": str(e)}
        logger.error("readiness_check_failed", component="redis", error=str(e))

    all_up = all(c["status"] == "up" for c in checks.values())
    status_code = 200 if all_up else 503

    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if all_up else "not_ready",
            "checks": checks,
        },
    )
