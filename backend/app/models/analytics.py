"""Analytics rollup models — derived, idempotent, rebuildable aggregates.

Each table is tenant-scoped, designed for fast dashboard reads, and
populated by incremental Celery jobs (never read from transactional tables
on the request path).  Every rollup carries an `as_of` timestamp.
"""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Index, Integer, Numeric,
    String, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


# ------------------------------------------------------------------
# Attendance rollups
# ------------------------------------------------------------------
class AnalyticsAttendanceDaily(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """School / class / section level attendance for a single day."""
    __tablename__ = "analytics_attendance_daily"

    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    class_id: Mapped[UUID | None] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=True)
    section_id: Mapped[UUID | None] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), nullable=True)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False)

    total_students: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    present_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    absent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    late_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    half_day_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    leave_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    excused_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    marked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "section_id", "attendance_date", name="uq_analytics_att_daily_section_date"),
        Index("ix_analytics_att_daily_school_date", "school_id", "attendance_date"),
    )


class AnalyticsAttendanceStudentMonth(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Per-student monthly attendance rollup."""
    __tablename__ = "analytics_attendance_student_month"

    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    month: Mapped[date] = mapped_column(Date, nullable=False)  # first day of month

    marked_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    weighted_present: Mapped[Decimal] = mapped_column(Numeric(7, 2), default=0, nullable=False)
    percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "student_id", "month", name="uq_analytics_att_student_month"),
    )


# ------------------------------------------------------------------
# Exam / academic rollups
# ------------------------------------------------------------------
class AnalyticsExamSubjectStats(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Subject-level statistics per exam per class/section."""
    __tablename__ = "analytics_exam_subject_stats"

    exam_id: Mapped[UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False, index=True)
    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    section_id: Mapped[UUID | None] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), nullable=True)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)

    average: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    median: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    min_score: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    max_score: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    pass_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    grade_distribution: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)  # {"A1": 5, "B2": 10, ...}
    absent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_students: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "exam_id", "section_id", "subject_id", name="uq_analytics_exam_subj_stats"),
        Index("ix_analytics_exam_stats_exam", "exam_id"),
    )


class AnalyticsExamStudentTrend(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Per-student exam trend for tracking progress."""
    __tablename__ = "analytics_exam_student_trend"

    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_id: Mapped[UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    percentage: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    grade: Mapped[str | None] = mapped_column(String(10), nullable=True)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "student_id", "exam_id", name="uq_analytics_exam_student_trend"),
    )


# ------------------------------------------------------------------
# Fee rollups
# ------------------------------------------------------------------
class AnalyticsFeeDaily(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Daily fee collection summary by mode and category."""
    __tablename__ = "analytics_fee_daily"

    collection_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_mode: Mapped[str | None] = mapped_column(String(30), nullable=True)  # cash, online, cheque, etc.
    category_id: Mapped[UUID | None] = mapped_column(ForeignKey("fee_categories.id", ondelete="SET NULL"), nullable=True)
    total_collected: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    transaction_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "collection_date", "payment_mode", "category_id", name="uq_analytics_fee_daily"),
        Index("ix_analytics_fee_daily_school_date", "school_id", "collection_date"),
    )


class AnalyticsFeeDuesSnapshot(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Daily snapshot of outstanding dues by class and aging bucket."""
    __tablename__ = "analytics_fee_dues_snapshot"

    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    class_id: Mapped[UUID | None] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=True)
    bucket_0_30: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    bucket_31_60: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    bucket_61_90: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    bucket_91_plus: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    total_dues: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    student_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "snapshot_date", "class_id", name="uq_analytics_fee_dues_snap"),
        Index("ix_analytics_fee_dues_school_date", "school_id", "snapshot_date"),
    )


# ------------------------------------------------------------------
# Homework rollup
# ------------------------------------------------------------------
class AnalyticsHomeworkSectionWeek(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Homework completion by section and week."""
    __tablename__ = "analytics_homework_section_week"

    section_id: Mapped[UUID] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
    week_start: Mapped[date] = mapped_column(Date, nullable=False)
    assigned_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    submitted_on_time: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    submitted_late: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pending_evaluation: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "section_id", "week_start", name="uq_analytics_hw_section_week"),
    )


# ------------------------------------------------------------------
# Curriculum rollup
# ------------------------------------------------------------------
class AnalyticsCurriculumSectionSubject(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Curriculum completion by section and subject."""
    __tablename__ = "analytics_curriculum_section_subject"

    section_id: Mapped[UUID] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    expected_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0, nullable=False)
    actual_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "section_id", "subject_id", "academic_year_id", name="uq_analytics_curr_sec_subj"),
    )


# ------------------------------------------------------------------
# Library rollup
# ------------------------------------------------------------------
class AnalyticsLibraryDaily(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Daily library activity summary."""
    __tablename__ = "analytics_library_daily"

    activity_date: Mapped[date] = mapped_column(Date, nullable=False)
    issues_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    returns_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    renewals_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    fines_assessed: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    fines_collected: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    active_loans: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    overdue_loans: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "activity_date", name="uq_analytics_library_daily"),
    )


# ------------------------------------------------------------------
# Transport rollup
# ------------------------------------------------------------------
class AnalyticsTransportDaily(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Daily transport operations summary."""
    __tablename__ = "analytics_transport_daily"

    run_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cancelled_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    delayed_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_riders: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    boarded_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    absent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "run_date", name="uq_analytics_transport_daily"),
    )


# ------------------------------------------------------------------
# Engagement rollup
# ------------------------------------------------------------------
class AnalyticsEngagementDaily(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Daily engagement / login summary by role."""
    __tablename__ = "analytics_engagement_daily"

    activity_date: Mapped[date] = mapped_column(Date, nullable=False)
    role_slug: Mapped[str] = mapped_column(String(30), nullable=False)
    active_users: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    login_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "activity_date", "role_slug", name="uq_analytics_engagement_daily"),
    )


# ------------------------------------------------------------------
# Teacher workload
# ------------------------------------------------------------------
class AnalyticsTeacherWorkload(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Weekly teacher workload metrics (descriptive, not evaluative)."""
    __tablename__ = "analytics_teacher_workload"

    staff_id: Mapped[UUID] = mapped_column(ForeignKey("staff.id", ondelete="CASCADE"), nullable=False, index=True)
    week_start: Mapped[date] = mapped_column(Date, nullable=False)
    scheduled_periods: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sections_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pending_evaluations: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pending_mark_sheets: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    substitutions_covered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "staff_id", "week_start", name="uq_analytics_teacher_workload"),
    )


# ------------------------------------------------------------------
# Rollup tracking
# ------------------------------------------------------------------
class RollupRun(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Tracks each rollup execution for audit and verification."""
    __tablename__ = "rollup_runs"

    rollup_key: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    window_start: Mapped[date] = mapped_column(Date, nullable=False)
    window_end: Mapped[date] = mapped_column(Date, nullable=False)
    rows_upserted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    watermark: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="completed", nullable=False)  # completed, failed, skipped
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_rollup_runs_key_window", "rollup_key", "window_start", "window_end"),
    )


# ------------------------------------------------------------------
# Student risk scores
# ------------------------------------------------------------------
class StudentRiskScore(Base, UUIDPrimaryKeyMixin, TenantMixin):
    """Transparent, rule-based risk indicators for students."""
    __tablename__ = "student_risk_scores"

    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0-100
    level: Mapped[str] = mapped_column(String(10), default="low", nullable=False)  # low, medium, high
    factors: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    # factors: [{"rule": "attendance_below_threshold", "value": 72.5, "threshold": 75, "weight": 30, "contribution": 30}]
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "student_id", "academic_year_id", name="uq_student_risk_score"),
        Index("ix_risk_score_level", "school_id", "level"),
    )
