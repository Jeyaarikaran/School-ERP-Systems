"""Homework and Assignment Models."""

from datetime import datetime
from uuid import UUID
import enum

from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, Enum as SQLEnum, UniqueConstraint, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class HomeworkStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"
    ARCHIVED = "archived"


class Homework(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "homework"

    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(5000), nullable=False)
    
    assigned_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    
    max_marks: Mapped[float | None] = mapped_column(Numeric(6,2), nullable=True)
    allow_late: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    late_cutoff_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    allow_text: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    allow_files: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    status: Mapped[HomeworkStatus] = mapped_column(SQLEnum(HomeworkStatus), default=HomeworkStatus.DRAFT, nullable=False)
    
    created_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class HomeworkTarget(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Which sections are assigned this homework."""
    __tablename__ = "homework_targets"

    homework_id: Mapped[UUID] = mapped_column(ForeignKey("homework.id", ondelete="CASCADE"), index=True, nullable=False)
    section_id: Mapped[UUID] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("homework_id", "section_id", name="uq_hw_target_section"),
    )


class HomeworkAttachment(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Files attached by the teacher."""
    __tablename__ = "homework_attachments"

    homework_id: Mapped[UUID] = mapped_column(ForeignKey("homework.id", ondelete="CASCADE"), index=True, nullable=False)
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file_metadata.id", ondelete="CASCADE"), nullable=False)


class SubmissionStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    LATE = "late"
    RETURNED = "returned"
    EVALUATED = "evaluated"


class HomeworkSubmission(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """The latest state of a student's submission."""
    __tablename__ = "homework_submissions"

    homework_id: Mapped[UUID] = mapped_column(ForeignKey("homework.id", ondelete="CASCADE"), index=True, nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    status: Mapped[SubmissionStatus] = mapped_column(SQLEnum(SubmissionStatus), nullable=False)
    text_answer: Mapped[str | None] = mapped_column(String(10000), nullable=True)
    
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_late: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    attempt_no: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    marks: Mapped[float | None] = mapped_column(Numeric(6,2), nullable=True)
    feedback: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    
    evaluated_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    evaluated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    submitted_by_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    on_behalf: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    client_submission_id: Mapped[str] = mapped_column(String(50), nullable=False) # Idempotency

    __table_args__ = (
        UniqueConstraint("homework_id", "student_id", name="uq_hw_submission_student"),
    )


class HomeworkSubmissionAttempt(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Append-only history of submission attempts."""
    __tablename__ = "homework_submission_attempts"

    submission_id: Mapped[UUID] = mapped_column(ForeignKey("homework_submissions.id", ondelete="CASCADE"), index=True, nullable=False)
    attempt_no: Mapped[int] = mapped_column(Integer, nullable=False)
    
    text_answer: Mapped[str | None] = mapped_column(String(10000), nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class HomeworkSubmissionFile(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Files attached to a specific attempt."""
    __tablename__ = "homework_submission_files"

    attempt_id: Mapped[UUID] = mapped_column(ForeignKey("homework_submission_attempts.id", ondelete="CASCADE"), index=True, nullable=False)
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file_metadata.id", ondelete="CASCADE"), nullable=False)
