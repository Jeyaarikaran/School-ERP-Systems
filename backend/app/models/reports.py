"""Report engine models — catalog, jobs, schedules, and file tracking.

The report engine unifies all exports into a single pipeline with
async generation, scope enforcement, and multi-format output.
"""

from datetime import datetime
from uuid import UUID
import enum

from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Index, Integer, Numeric,
    String, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class ReportJobStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class ReportJob(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Tracks an async report generation job."""
    __tablename__ = "report_jobs"

    requester_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    definition_key: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    params: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    format: Mapped[str] = mapped_column(String(10), nullable=False)  # csv, xlsx, pdf
    status: Mapped[ReportJobStatus] = mapped_column(
        default=ReportJobStatus.QUEUED, nullable=False
    )
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0-100
    row_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    file_id: Mapped[UUID | None] = mapped_column(ForeignKey("file_metadata.id", ondelete="SET NULL"), nullable=True)
    file_storage_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)  # SHA-256
    error_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_sensitive: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)  # required for sensitive reports

    queued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # For schedule-generated jobs
    schedule_id: Mapped[UUID | None] = mapped_column(ForeignKey("report_schedules.id", ondelete="SET NULL"), nullable=True)
    period_key: Mapped[str | None] = mapped_column(String(30), nullable=True)  # e.g. "2026-W40" for weekly

    __table_args__ = (
        Index("ix_report_jobs_requester_status", "requester_id", "status"),
        Index("ix_report_jobs_school_status", "school_id", "status"),
        UniqueConstraint("schedule_id", "period_key", name="uq_report_jobs_schedule_period"),
    )


class ReportScheduleFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ReportScheduleStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    DELETED = "deleted"


class ReportSchedule(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Recurring report generation schedule."""
    __tablename__ = "report_schedules"

    definition_key: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    params: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    format: Mapped[str] = mapped_column(String(10), nullable=False)
    frequency: Mapped[ReportScheduleFrequency] = mapped_column(nullable=False)
    day_of_week: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 0=Mon, 6=Sun (weekly)
    day_of_month: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1-28 (monthly)
    time_of_day: Mapped[str] = mapped_column(String(5), nullable=False, default="06:00")  # HH:MM in school tz
    timezone: Mapped[str] = mapped_column(String(50), nullable=False, default="Asia/Kolkata")
    recipients: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)  # list of user_ids (internal only)

    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[ReportScheduleStatus] = mapped_column(
        default=ReportScheduleStatus.ACTIVE, nullable=False
    )
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_report_schedules_next_run", "status", "next_run_at"),
    )
