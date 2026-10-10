"""Attendance and Offline Sync Models."""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import String, Integer, ForeignKey, Date, DateTime, JSON, Enum as SQLEnum, UniqueConstraint, Index, CheckConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class DayType(str, enum.Enum):
    WORKING = "working"
    HOLIDAY = "holiday"
    HALF_DAY = "half_day"
    EXAM_DAY = "exam_day"


class SchoolCalendarDay(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Calendar overrides and defined holidays."""
    __tablename__ = "school_calendar_days"

    date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    day_type: Mapped[DayType] = mapped_column(SQLEnum(DayType), default=DayType.WORKING, nullable=False)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name_local: Mapped[str | None] = mapped_column(String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint("school_id", "date", name="uq_calendar_date_school"),
    )


class SessionState(str, enum.Enum):
    OPEN = "open"
    SUBMITTED = "submitted"
    LOCKED = "locked"


class AttendanceSession(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """A daily attendance session for a section."""
    __tablename__ = "attendance_sessions"

    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id"), nullable=False, index=True)
    section_id: Mapped[UUID] = mapped_column(ForeignKey("sections.id"), nullable=False, index=True)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False)
    session_type: Mapped[str] = mapped_column(String(20), default="daily", nullable=False)
    
    state: Mapped[SessionState] = mapped_column(SQLEnum(SessionState), default=SessionState.OPEN, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    submitted_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    server_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("section_id", "attendance_date", "session_type", name="uq_session_section_date_type"),
        Index("ix_attendance_session_school_date_state", "school_id", "attendance_date", "state"),
    )
    
    records = relationship("AttendanceRecord", back_populates="session", cascade="all, delete-orphan")


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    LEAVE = "leave"
    EXCUSED = "excused"


class RecordSource(str, enum.Enum):
    ONLINE = "online"
    OFFLINE_SYNC = "offline_sync"
    CORRECTION = "correction"


class AttendanceRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Individual student attendance records."""
    __tablename__ = "attendance_records"

    session_id: Mapped[UUID] = mapped_column(ForeignKey("attendance_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    enrollment_id: Mapped[UUID] = mapped_column(ForeignKey("student_enrollments.id", ondelete="CASCADE"), nullable=False)
    
    # Denormalized for rapid querying and partitioning
    attendance_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    
    status: Mapped[AttendanceStatus] = mapped_column(SQLEnum(AttendanceStatus), nullable=False)
    arrival_time: Mapped[str | None] = mapped_column(String(5), nullable=True) # HH:MM format for late
    remarks: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    marked_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    client_marked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    server_received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    source: Mapped[RecordSource] = mapped_column(SQLEnum(RecordSource), nullable=False)
    record_version: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("session_id", "student_id", name="uq_record_session_student"),
        Index("ix_record_student_date", "student_id", "attendance_date"),
        Index("ix_record_school_date_status", "school_id", "attendance_date", "status"),
    )
    
    session = relationship("AttendanceSession", back_populates="records")


class CorrectionStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_APPROVED = "auto_approved"


class AttendanceCorrection(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Requests and approvals for attendance changes."""
    __tablename__ = "attendance_corrections"
    
    record_id: Mapped[UUID | None] = mapped_column(ForeignKey("attendance_records.id", ondelete="CASCADE"), index=True, nullable=True)
    session_id: Mapped[UUID] = mapped_column(ForeignKey("attendance_sessions.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    old_status: Mapped[AttendanceStatus | None] = mapped_column(SQLEnum(AttendanceStatus), nullable=True)
    new_status: Mapped[AttendanceStatus] = mapped_column(SQLEnum(AttendanceStatus), nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    
    requested_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    status: Mapped[CorrectionStatus] = mapped_column(SQLEnum(CorrectionStatus), default=CorrectionStatus.PENDING, nullable=False)
    
    decided_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    decision_note: Mapped[str | None] = mapped_column(String(255), nullable=True)


class AttendanceHistory(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Immutable audit trail for every change to a record."""
    __tablename__ = "attendance_history"
    
    record_id: Mapped[UUID] = mapped_column(ForeignKey("attendance_records.id", ondelete="CASCADE"), index=True, nullable=False)
    old_status: Mapped[AttendanceStatus | None] = mapped_column(SQLEnum(AttendanceStatus), nullable=True)
    new_status: Mapped[AttendanceStatus] = mapped_column(SQLEnum(AttendanceStatus), nullable=False)
    remarks: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    changed_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source: Mapped[RecordSource] = mapped_column(SQLEnum(RecordSource), nullable=False)
    correction_request_id: Mapped[UUID | None] = mapped_column(ForeignKey("attendance_corrections.id", ondelete="SET NULL"), nullable=True)


class AttendanceSyncOp(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Idempotency store for offline batch sync requests."""
    __tablename__ = "attendance_sync_ops"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    client_op_id: Mapped[str] = mapped_column(String(50), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    result: Mapped[dict] = mapped_column(JSONB, nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "user_id", "client_op_id", name="uq_sync_op_client_id"),
    )


class AttendanceDailySummary(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Aggregated daily cache for fast dashboard reading."""
    __tablename__ = "attendance_daily_summary"
    
    session_id: Mapped[UUID] = mapped_column(ForeignKey("attendance_sessions.id", ondelete="CASCADE"), unique=True, nullable=False)
    attendance_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    
    total_students: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    present_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    absent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    late_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    half_day_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    leave_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    excused_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    is_submitted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class OutboxEvent(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Domain events outbox table."""
    __tablename__ = "outbox_events"
    
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    aggregate_type: Mapped[str] = mapped_column(String(50), nullable=False)
    aggregate_id: Mapped[UUID] = mapped_column(nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        # Index on unpublished events for fast polling
        Index("ix_outbox_unpublished", "published_at", postgresql_where="published_at IS NULL"),
    )
