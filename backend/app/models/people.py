"""People models: Students, Guardians, Staff, and Enrollments."""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import String, Integer, Boolean, ForeignKey, Date, DateTime, JSON, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship as orm_relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class StudentStatus(str, enum.Enum):
    ACTIVE = "active"
    TRANSFERRED = "transferred"
    GRADUATED = "graduated"
    WITHDRAWN = "withdrawn"
    ARCHIVED = "archived"


class Student(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Student profiles."""
    __tablename__ = "students"

    admission_no: Mapped[str] = mapped_column(String(50), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    name_local: Mapped[str | None] = mapped_column(String(150), nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    blood_group: Mapped[str | None] = mapped_column(String(10), nullable=True)
    
    # Sensitive contact info
    address: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    emergency_contact: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    
    photo_file_id: Mapped[UUID | None] = mapped_column(ForeignKey("file_metadata.id", ondelete="SET NULL"), nullable=True)
    admission_date: Mapped[date] = mapped_column(Date, nullable=False)
    previous_school: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    status: Mapped[StudentStatus] = mapped_column(SQLEnum(StudentStatus), default=StudentStatus.ACTIVE, nullable=False)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, unique=True)
    branch_id: Mapped[UUID | None] = mapped_column(ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)

    __table_args__ = (
        UniqueConstraint("school_id", "admission_no", name="uq_school_admission_no"),
    )

    enrollments = orm_relationship("StudentEnrollment", back_populates="student", cascade="all, delete-orphan")
    guardian_links = orm_relationship("StudentGuardian", back_populates="student", cascade="all, delete-orphan")


class Guardian(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Parent/Guardian profiles. Shared across multiple students."""
    __tablename__ = "guardians"

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)  # Normalized E.164
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, unique=True)

    __table_args__ = (
        UniqueConstraint("school_id", "phone", name="uq_school_guardian_phone"),
    )

    student_links = orm_relationship("StudentGuardian", back_populates="guardian", cascade="all, delete-orphan")


class StudentGuardian(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Many-to-many link between students and guardians."""
    __tablename__ = "student_guardians"

    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    guardian_id: Mapped[UUID] = mapped_column(ForeignKey("guardians.id", ondelete="CASCADE"), index=True, nullable=False)
    
    relationship: Mapped[str] = mapped_column(String(50), nullable=False)  # Father, Mother, Uncle, etc.
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_emergency_contact: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    can_pickup: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_financial_responsible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("student_id", "guardian_id", name="uq_student_guardian_link"),
    )

    student = orm_relationship("Student", back_populates="guardian_links")
    guardian = orm_relationship("Guardian", back_populates="student_links")


class EnrollmentStatus(str, enum.Enum):
    ENROLLED = "enrolled"
    PROMOTED = "promoted"
    REPEATED = "repeated"
    TRANSFERRED_OUT = "transferred_out"
    GRADUATED = "graduated"
    WITHDRAWN = "withdrawn"


class StudentEnrollment(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Student enrollment record for a specific academic year and section."""
    __tablename__ = "student_enrollments"

    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)
    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), index=True, nullable=False)
    section_id: Mapped[UUID] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), index=True, nullable=False)
    branch_id: Mapped[UUID | None] = mapped_column(ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    
    roll_no: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[EnrollmentStatus] = mapped_column(SQLEnum(EnrollmentStatus), default=EnrollmentStatus.ENROLLED, nullable=False)
    
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    __table_args__ = (
        UniqueConstraint("student_id", "academic_year_id", name="uq_student_enrollment_year"),
        UniqueConstraint("section_id", "roll_no", name="uq_section_roll_no"),  # Re-assigned on section transfer
    )

    student = orm_relationship("Student", back_populates="enrollments")


class StudentStatusHistory(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Append-only history of student status and section transfers."""
    __tablename__ = "student_status_history"

    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    change_type: Mapped[str] = mapped_column(String(50), nullable=False)  # status_change, section_transfer, promotion
    from_value: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    to_value: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    performed_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(36), nullable=True)


class StaffStatus(str, enum.Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    RESIGNED = "resigned"
    TERMINATED = "terminated"
    ARCHIVED = "archived"


class Staff(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """All school employees."""
    __tablename__ = "staff"

    employee_code: Mapped[str] = mapped_column(String(50), nullable=False)
    staff_type: Mapped[str] = mapped_column(String(50), nullable=False)  # teacher, principal, support, etc.
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    designation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    joining_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[StaffStatus] = mapped_column(SQLEnum(StaffStatus), default=StaffStatus.ACTIVE, nullable=False)
    
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, unique=True)
    branch_id: Mapped[UUID | None] = mapped_column(ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)

    __table_args__ = (
        UniqueConstraint("school_id", "employee_code", name="uq_school_employee_code"),
    )


class Teacher(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """1:1 extension of Staff for teachers."""
    __tablename__ = "teachers"

    staff_id: Mapped[UUID] = mapped_column(ForeignKey("staff.id", ondelete="CASCADE"), unique=True, nullable=False)
    specialization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    qualification: Mapped[str | None] = mapped_column(String(255), nullable=True)
    max_weekly_periods: Mapped[int | None] = mapped_column(Integer, nullable=True)


class TeacherSubject(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Assignments linking a teacher to a section and subject. Drives Teacher row-scope."""
    __tablename__ = "teacher_subjects"

    teacher_id: Mapped[UUID] = mapped_column(ForeignKey("staff.id", ondelete="CASCADE"), index=True, nullable=False)
    section_id: Mapped[UUID] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), index=True, nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), index=True, nullable=False)
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("teacher_id", "section_id", "subject_id", "academic_year_id", name="uq_teacher_assignment"),
    )
