"""Application error hierarchy and exception handlers."""

from typing import Any
from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import structlog

logger = structlog.get_logger()


class AppError(Exception):
    """Base application error. All domain errors extend this."""

    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred"

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        self.message = message or self.__class__.message
        self.error_code = code or self.__class__.error_code
        self.details = details or []
        super().__init__(self.message)


class ValidationError(AppError):
    status_code = 400
    error_code = "VALIDATION_ERROR"
    message = "Request validation failed"


class BadRequestError(AppError):
    status_code = 400
    error_code = "BAD_REQUEST"
    message = "Malformed request"


class AuthenticationError(AppError):
    status_code = 401
    error_code = "UNAUTHORIZED"
    message = "Authentication required"


class TokenExpiredError(AppError):
    status_code = 401
    error_code = "TOKEN_EXPIRED"
    message = "Access token has expired"


class InvalidCredentialsError(AppError):
    status_code = 401
    error_code = "INVALID_CREDENTIALS"
    message = "Invalid email or password"


class AuthorizationError(AppError):
    status_code = 403
    error_code = "FORBIDDEN"
    message = "Insufficient permissions"


class TenantMismatchError(AppError):
    status_code = 403
    error_code = "TENANT_MISMATCH"
    message = "Access denied"


class NotFoundError(AppError):
    status_code = 404
    error_code = "NOT_FOUND"
    message = "Resource not found"


class ConflictError(AppError):
    status_code = 409
    error_code = "CONFLICT"
    message = "Resource already exists"


class StateConflictError(AppError):
    status_code = 409
    error_code = "STATE_CONFLICT"
    message = "Invalid state transition"


class UnprocessableError(AppError):
    status_code = 422
    error_code = "UNPROCESSABLE_ENTITY"
    message = "Request is semantically invalid"


class RateLimitError(AppError):
    status_code = 429
    error_code = "RATE_LIMITED"
    message = "Too many requests"


class GatewayError(AppError):
    status_code = 502
    error_code = "GATEWAY_ERROR"
    message = "Upstream service unavailable"


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.warning(
            "app_error",
            error_code=exc.error_code,
            message=exc.message,
            status_code=exc.status_code,
            request_id=str(request_id) if request_id else None,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.details,
                },
                "meta": {
                    "request_id": str(request_id) if request_id else None,
                },
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.exception(
            "unhandled_error",
            error=str(exc),
            request_id=str(request_id) if request_id else None,
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                    "details": [],
                },
                "meta": {
                    "request_id": str(request_id) if request_id else None,
                },
            },
        )
