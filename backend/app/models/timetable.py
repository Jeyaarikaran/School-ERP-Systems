"""Timetable and Bell Schedule Models."""

from datetime import date, time, datetime
from uuid import UUID
import enum

from sqlalchemy import String, Integer, ForeignKey, Date, Time, DateTime, Enum as SQLEnum, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import DATERANGE

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class PeriodType(str, enum.Enum):
    CLASS = "class"
    BREAK = "break"
    LUNCH = "lunch"
    ASSEMBLY = "assembly"


class BellSchedule(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """A bell schedule (e.g., 'Regular', 'Half Day')."""
    __tablename__ = "bell_schedules"

    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "academic_year_id", "name", name="uq_bell_schedule_name"),
    )
    periods = relationship("BellSchedulePeriod", back_populates="schedule", cascade="all, delete-orphan")


class BellSchedulePeriod(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Periods within a bell schedule."""
    __tablename__ = "bell_schedule_periods"

    schedule_id: Mapped[UUID] = mapped_column(ForeignKey("bell_schedules.id", ondelete="CASCADE"), index=True, nullable=False)
    period_no: Mapped[int] = mapped_column(Integer, nullable=False)
    label: Mapped[str] = mapped_column(String(50), nullable=False)
    label_local: Mapped[str | None] = mapped_column(String(50), nullable=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    period_type: Mapped[PeriodType] = mapped_column(SQLEnum(PeriodType), nullable=False)

    schedule = relationship("BellSchedule", back_populates="periods")


class BellScheduleDay(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Maps 0-6 (Mon-Sun) to a schedule per year."""
    __tablename__ = "bell_schedule_days"

    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)
    weekday: Mapped[int] = mapped_column(Integer, nullable=False) # 0=Monday, 6=Sunday
    schedule_id: Mapped[UUID] = mapped_column(ForeignKey("bell_schedules.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("academic_year_id", "weekday", name="uq_bell_schedule_weekday"),
    )


class TimetableStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    SUPERSEDED = "superseded"


class Timetable(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Versioned timetable for a section."""
    __tablename__ = "timetables"

    section_id: Mapped[UUID] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), index=True, nullable=False)
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    
    version_no: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[TimetableStatus] = mapped_column(SQLEnum(TimetableStatus), default=TimetableStatus.DRAFT, nullable=False)
    
    effective_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    
    published_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("section_id", "version_no", name="uq_timetable_version"),
        Index("ix_timetable_effective", "section_id", "status", "effective_from", "effective_to"),
    )
    entries = relationship("TimetableEntry", back_populates="timetable", cascade="all, delete-orphan")


class EntryType(str, enum.Enum):
    REGULAR = "regular"
    LAB = "lab"
    ACTIVITY = "activity"


class TimetableEntry(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Individual slots in a timetable."""
    __tablename__ = "timetable_entries"

    timetable_id: Mapped[UUID] = mapped_column(ForeignKey("timetables.id", ondelete="CASCADE"), index=True, nullable=False)
    weekday: Mapped[int] = mapped_column(Integer, nullable=False)
    period_id: Mapped[UUID] = mapped_column(ForeignKey("bell_schedule_periods.id", ondelete="CASCADE"), nullable=False)
    
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    teacher_id: Mapped[UUID] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"), index=True, nullable=False)
    room_id: Mapped[UUID | None] = mapped_column(ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    
    entry_type: Mapped[EntryType] = mapped_column(SQLEnum(EntryType), default=EntryType.REGULAR, nullable=False)

    timetable = relationship("Timetable", back_populates="entries")


class ResourceType(str, enum.Enum):
    TEACHER = "teacher"
    ROOM = "room"
    SECTION = "section"


class TimetableSlotClaim(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """
    Conflict prevention table. Uses PostgreSQL EXCLUDE USING gist to physically 
    prevent overlapping schedules across date ranges for teachers, rooms, or sections.
    """
    __tablename__ = "timetable_slot_claims"

    timetable_id: Mapped[UUID] = mapped_column(ForeignKey("timetables.id", ondelete="CASCADE"), nullable=False)
    entry_id: Mapped[UUID] = mapped_column(ForeignKey("timetable_entries.id", ondelete="CASCADE"), nullable=False)
    
    weekday: Mapped[int] = mapped_column(Integer, nullable=False)
    period_id: Mapped[UUID] = mapped_column(ForeignKey("bell_schedule_periods.id", ondelete="CASCADE"), nullable=False)
    
    resource_type: Mapped[ResourceType] = mapped_column(SQLEnum(ResourceType), nullable=False)
    resource_id: Mapped[UUID] = mapped_column(nullable=False) # Represents Teacher, Room, or Section UUID
    
    effective_range: Mapped[str] = mapped_column(DATERANGE, nullable=False)

    # Note: Alembic will need `CREATE EXTENSION btree_gist;` manually added before creating this table
    # The actual constraint is applied via SQLAlchemy Index/Constraint definitions, 
    # but since SQLAlchemy's ExcludeConstraint syntax is complex and heavily dialect-specific,
    # we document the RAW SQL equivalent that will be injected via migration:
    # EXCLUDE USING gist (school_id WITH =, weekday WITH =, period_id WITH =, resource_type WITH =, resource_id WITH =, effective_range WITH &&)
