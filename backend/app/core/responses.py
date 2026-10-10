"""Standard API response envelope models."""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Offset pagination metadata."""

    page: int
    limit: int
    total: int
    total_pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1


class CursorPaginationMeta(BaseModel):
    """Cursor pagination metadata."""

    cursor: str | None = None
    next_cursor: str | None = None
    has_next: bool = False
    limit: int = 50


class ResponseMeta(BaseModel):
    """Response metadata included in every response."""

    request_id: str | None = None
    timestamp: str | None = None
    pagination: PaginationMeta | CursorPaginationMeta | None = None


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response envelope."""

    success: bool = True
    data: T
    message: str = "OPERATION_COMPLETED"
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class ErrorDetail(BaseModel):
    """Individual validation error detail."""

    field: str | None = None
    message: str
    code: str | None = None


class ErrorBody(BaseModel):
    """Error payload."""

    code: str
    message: str
    details: list[ErrorDetail] = []


class ErrorResponse(BaseModel):
    """Standard error response envelope."""

    success: bool = False
    error: ErrorBody
    meta: ResponseMeta = Field(default_factory=ResponseMeta)
