"""Academic structure models: Years, Classes, Sections, Subjects, and Rooms."""

from datetime import date
from uuid import UUID

from sqlalchemy import String, Integer, Boolean, ForeignKey, UniqueConstraint, Date, Enum as SQLEnum, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class AcademicYearStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class AcademicYear(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """School academic year boundary."""
    __tablename__ = "academic_years"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[AcademicYearStatus] = mapped_column(SQLEnum(AcademicYearStatus), default=AcademicYearStatus.DRAFT, nullable=False)

    __table_args__ = (
        CheckConstraint("end_date > start_date", name="chk_academic_year_dates"),
        # Only one active year per school
        Index("ix_academic_year_active_school", "school_id", unique=True, postgresql_where="status = 'ACTIVE'"),
        # Exclusion constraint requires btree_gist extension (handled in migration)
    )

    sections = relationship("Section", back_populates="academic_year", cascade="all, delete-orphan")


class ClassLevel(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Grade level definition (e.g., Grade 10)."""
    __tablename__ = "classes"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_class_name_school"),
    )

    sections = relationship("Section", back_populates="class_level", cascade="all, delete-orphan")


class Room(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Physical rooms."""
    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="classroom")
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=30)

    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_room_name_school"),
    )


class Section(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Specific section of a class in an academic year (e.g., 10-A, 2024-25)."""
    __tablename__ = "sections"

    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), index=True, nullable=False)
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=40)
    
    # Deferred foreign key to staff, assuming staff table is defined later
    class_teacher_id: Mapped[UUID | None] = mapped_column(ForeignKey("staff.id", ondelete="SET NULL"), nullable=True, index=True)
    room_id: Mapped[UUID | None] = mapped_column(ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True, index=True)

    __table_args__ = (
        UniqueConstraint("class_id", "academic_year_id", "name", name="uq_section_name_year"),
    )

    class_level = relationship("ClassLevel", back_populates="sections")
    academic_year = relationship("AcademicYear", back_populates="sections")


class SubjectType(str, enum.Enum):
    CORE = "core"
    ELECTIVE = "elective"
    CO_SCHOLASTIC = "co_scholastic"
    PRACTICAL = "practical"


class Subject(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """School subject catalog."""
    __tablename__ = "subjects"

    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    name_local: Mapped[str | None] = mapped_column(String(100), nullable=True)
    type: Mapped[SubjectType] = mapped_column(SQLEnum(SubjectType), default=SubjectType.CORE, nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "code", name="uq_subject_code_school"),
    )


class ClassSubject(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Mapping of subjects taught in a class for a specific year."""
    __tablename__ = "class_subjects"

    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), index=True, nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), index=True, nullable=False)
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)
    
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    weekly_periods: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint("class_id", "subject_id", "academic_year_id", name="uq_class_subject_year"),
    )


class CodeCounter(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Atomic counter for admission/employee codes."""
    __tablename__ = "code_counters"

    counter_key: Mapped[str] = mapped_column(String(50), nullable=False)
    next_value: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __table_args__ = (
        UniqueConstraint("school_id", "counter_key", name="uq_school_counter_key"),
    )
