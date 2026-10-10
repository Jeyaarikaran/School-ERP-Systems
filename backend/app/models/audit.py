"""Audit and Idempotency models."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin


class AuditLog(Base, UUIDPrimaryKeyMixin):
    """Append-only audit log."""
    __tablename__ = "audit_logs"

    school_id: Mapped[UUID | None] = mapped_column(ForeignKey("schools.id"), nullable=True, index=True)
    actor_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    actor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    old_value: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    
    # Needs to be primary key component for partitioning in Postgres
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)


class IdempotencyKey(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Storage for idempotency keys."""
    __tablename__ = "idempotency_keys"

    school_id: Mapped[UUID | None] = mapped_column(ForeignKey("schools.id"), nullable=True, index=True)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    request_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    response_status: Mapped[int | None] = mapped_column(nullable=True)
    response_body: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    state: Mapped[str] = mapped_column(String(20), default="in_progress", nullable=False)  # in_progress, completed
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
