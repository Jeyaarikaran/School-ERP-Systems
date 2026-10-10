"""Structured logging configuration — structlog with JSON output and sensitive field redaction."""

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict

from app.core.config import settings

# Fields to redact in logs
SENSITIVE_FIELDS = frozenset({
    "password",
    "password_hash",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "authorization",
    "otp",
    "code",
    "api_key",
    "secret_key",
    "credit_card",
    "aadhaar",
})


def redact_sensitive_fields(
    logger: Any, method_name: str, event_dict: EventDict
) -> EventDict:
    """Redact sensitive fields from log output."""
    for key in list(event_dict.keys()):
        if any(sensitive in key.lower() for sensitive in SENSITIVE_FIELDS):
            event_dict[key] = "***REDACTED***"
    return event_dict


def setup_logging() -> None:
    """Configure structlog and stdlib logging."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # Renderer based on environment
    if settings.log_format == "console":
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            redact_sensitive_fields,
            renderer,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
