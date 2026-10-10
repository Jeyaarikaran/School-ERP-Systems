"""Curriculum Tracking Models."""

from datetime import date, datetime
from uuid import UUID
import enum

from sqlalchemy import String, Integer, ForeignKey, Date, DateTime, Enum as SQLEnum, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class CurriculumUnit(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """A unit in the syllabus."""
    __tablename__ = "curriculum_units"

    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)
    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    
    unit_no: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    title_local: Mapped[str | None] = mapped_column(String(150), nullable=True)
    
    planned_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    planned_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    planned_periods: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    __table_args__ = (
        UniqueConstraint("academic_year_id", "class_id", "subject_id", "unit_no", name="uq_curriculum_unit_no"),
    )


class ProgressStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class CurriculumProgress(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Per-section progress tracking for a curriculum unit."""
    __tablename__ = "curriculum_progress"

    unit_id: Mapped[UUID] = mapped_column(ForeignKey("curriculum_units.id", ondelete="CASCADE"), nullable=False)
    section_id: Mapped[UUID] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), index=True, nullable=False)
    
    status: Mapped[ProgressStatus] = mapped_column(SQLEnum(ProgressStatus), default=ProgressStatus.PLANNED, nullable=False)
    actual_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    
    note: Mapped[str | None] = mapped_column(String(500), nullable=True)
    delay_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    updated_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    __table_args__ = (
        UniqueConstraint("unit_id", "section_id", name="uq_curriculum_progress_unit_section"),
    )


class CurriculumProgressHistory(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Append-only audit history of progress changes."""
    __tablename__ = "curriculum_progress_history"

    progress_id: Mapped[UUID] = mapped_column(ForeignKey("curriculum_progress.id", ondelete="CASCADE"), index=True, nullable=False)
    
    old_status: Mapped[ProgressStatus | None] = mapped_column(SQLEnum(ProgressStatus), nullable=True)
    new_status: Mapped[ProgressStatus] = mapped_column(SQLEnum(ProgressStatus), nullable=False)
    
    changed_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
