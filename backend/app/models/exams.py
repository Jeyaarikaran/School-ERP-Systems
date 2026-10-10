"""Examinations, Marks, and Results Models."""

from datetime import date, datetime
from uuid import UUID
import enum

from sqlalchemy import String, Integer, ForeignKey, Date, DateTime, Boolean, Numeric, Enum as SQLEnum, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, DATERANGE, TSTZRANGE

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


# ---------------------------------------------------------
# Grading Systems
# ---------------------------------------------------------
class GradingKind(str, enum.Enum):
    PERCENTAGE_BANDS = "percentage_bands"
    GPA = "gpa"

class RoundingMode(str, enum.Enum):
    HALF_UP = "HALF_UP"

class GradingSystem(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "grading_systems"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    kind: Mapped[GradingKind] = mapped_column(SQLEnum(GradingKind), nullable=False)
    pass_percentage: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    gpa_scale_max: Mapped[float | None] = mapped_column(Numeric(4,2), nullable=True)
    rounding: Mapped[RoundingMode] = mapped_column(SQLEnum(RoundingMode), default=RoundingMode.HALF_UP, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class GradeBand(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "grade_bands"
    
    grading_system_id: Mapped[UUID] = mapped_column(ForeignKey("grading_systems.id", ondelete="CASCADE"), index=True, nullable=False)
    min_percent: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    max_percent: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    grade_label: Mapped[str] = mapped_column(String(10), nullable=False)
    grade_point: Mapped[float] = mapped_column(Numeric(4,2), nullable=False)
    remark: Mapped[str | None] = mapped_column(String(100), nullable=True)
    remark_local: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_fail: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Note: Alembic will need `EXCLUDE USING gist (grading_system_id WITH =, numrange(min_percent, max_percent) WITH &&)`
    # To prevent overlapping grade bands at the database layer.


# ---------------------------------------------------------
# Exam Configuration
# ---------------------------------------------------------
class ExamStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    MARKS_ENTRY = "marks_entry"
    UNDER_REVIEW = "under_review"
    PUBLISHED = "published"

class ExamType(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "exam_types"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    default_grading_system_id: Mapped[UUID | None] = mapped_column(ForeignKey("grading_systems.id", ondelete="SET NULL"), nullable=True)

class Exam(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "exams"
    
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)
    exam_type_id: Mapped[UUID] = mapped_column(ForeignKey("exam_types.id", ondelete="RESTRICT"), nullable=False)
    grading_system_id: Mapped[UUID] = mapped_column(ForeignKey("grading_systems.id", ondelete="RESTRICT"), nullable=False)
    
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    name_local: Mapped[str | None] = mapped_column(String(150), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    status: Mapped[ExamStatus] = mapped_column(SQLEnum(ExamStatus), default=ExamStatus.DRAFT, nullable=False)
    results_published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    publish_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    grading_snapshot: Mapped[dict | None] = mapped_column(JSONB, nullable=True) # Frozen grading rules at publish

class ExamClass(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "exam_classes"
    exam_id: Mapped[UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    
    __table_args__ = (UniqueConstraint("exam_id", "class_id", name="uq_exam_class"),)

class ScoringType(str, enum.Enum):
    NUMERIC = "numeric"
    GRADE_ONLY = "grade_only"

class ExamSubject(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "exam_subjects"
    exam_id: Mapped[UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    
    scoring: Mapped[ScoringType] = mapped_column(SQLEnum(ScoringType), default=ScoringType.NUMERIC, nullable=False)
    credit_weight: Mapped[float] = mapped_column(Numeric(5,2), default=1.0, nullable=False)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    __table_args__ = (UniqueConstraint("exam_id", "class_id", "subject_id", name="uq_exam_subject"),)

class ExamComponent(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "exam_components"
    exam_subject_id: Mapped[UUID] = mapped_column(ForeignKey("exam_subjects.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False) # Theory, Practical, Internal
    max_marks: Mapped[float] = mapped_column(Numeric(6,2), nullable=False)
    pass_marks: Mapped[float] = mapped_column(Numeric(6,2), nullable=False)
    must_pass: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class StudentSubjectEnrollment(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "student_subject_enrollments"
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    
    __table_args__ = (UniqueConstraint("student_id", "academic_year_id", "subject_id", name="uq_student_elective"),)


# ---------------------------------------------------------
# Exam Scheduling (Conflict constraints via GIST)
# ---------------------------------------------------------
class ScheduleStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"

class ExamSchedule(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "exam_schedules"
    exam_id: Mapped[UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[ScheduleStatus] = mapped_column(SQLEnum(ScheduleStatus), default=ScheduleStatus.ACTIVE, nullable=False)
    
    # Needs EXCLUDE USING gist (class_id WITH =, tstzrange(starts_at, ends_at) WITH &&) WHERE (status = 'active')

class ExamInvigilation(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "exam_invigilations"
    schedule_id: Mapped[UUID] = mapped_column(ForeignKey("exam_schedules.id", ondelete="CASCADE"), index=True, nullable=False)
    room_id: Mapped[UUID] = mapped_column(ForeignKey("rooms.id", ondelete="RESTRICT"), nullable=False)
    staff_id: Mapped[UUID] = mapped_column(ForeignKey("staff.id", ondelete="RESTRICT"), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[ScheduleStatus] = mapped_column(SQLEnum(ScheduleStatus), default=ScheduleStatus.ACTIVE, nullable=False)

    # Needs EXCLUDE USING gist (room_id WITH =, tstzrange(starts_at, ends_at) WITH &&) WHERE (status = 'active')
    # Needs EXCLUDE USING gist (staff_id WITH =, tstzrange(starts_at, ends_at) WITH &&) WHERE (status = 'active')


# ---------------------------------------------------------
# Marks Entry
# ---------------------------------------------------------
class SheetState(str, enum.Enum):
    NOT_STARTED = "not_started"
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REOPENED = "reopened"

class MarkSheet(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "mark_sheets"
    exam_subject_id: Mapped[UUID] = mapped_column(ForeignKey("exam_subjects.id", ondelete="CASCADE"), nullable=False)
    section_id: Mapped[UUID] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
    
    state: Mapped[SheetState] = mapped_column(SQLEnum(SheetState), default=SheetState.NOT_STARTED, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    entered_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    submitted_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    approved_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reopen_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)

    __table_args__ = (UniqueConstraint("exam_subject_id", "section_id", name="uq_mark_sheet"),)


class MarkAttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    EXEMPT = "exempt"
    WITHHELD = "withheld"

class Mark(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "marks"
    mark_sheet_id: Mapped[UUID] = mapped_column(ForeignKey("mark_sheets.id", ondelete="CASCADE"), nullable=False)
    component_id: Mapped[UUID] = mapped_column(ForeignKey("exam_components.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    marks_obtained: Mapped[float | None] = mapped_column(Numeric(6,2), nullable=True)
    attendance_status: Mapped[MarkAttendanceStatus] = mapped_column(SQLEnum(MarkAttendanceStatus), default=MarkAttendanceStatus.PRESENT, nullable=False)
    grade_label: Mapped[str | None] = mapped_column(String(10), nullable=True) # for grade_only subjects
    
    entered_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    entered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    __table_args__ = (UniqueConstraint("mark_sheet_id", "component_id", "student_id", name="uq_mark_student"),)
    # Also needs a Postgres CHECK constraint: CHECK (marks_obtained >= 0 AND (attendance_status = 'present' OR marks_obtained IS NULL))


class MarkSource(str, enum.Enum):
    ENTRY = "entry"
    IMPORT = "import"
    CORRECTION = "correction"

class MarksHistory(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "marks_history"
    mark_id: Mapped[UUID] = mapped_column(ForeignKey("marks.id", ondelete="CASCADE"), index=True, nullable=False)
    old_value: Mapped[float | None] = mapped_column(Numeric(6,2), nullable=True)
    new_value: Mapped[float | None] = mapped_column(Numeric(6,2), nullable=True)
    
    changed_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source: Mapped[MarkSource] = mapped_column(SQLEnum(MarkSource), nullable=False)


# ---------------------------------------------------------
# Results and Report Cards
# ---------------------------------------------------------
class OverallResult(str, enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    INCOMPLETE = "incomplete"
    WITHHELD = "withheld"

class ExamSubjectResult(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "exam_subject_results"
    exam_id: Mapped[UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    
    total_obtained: Mapped[float | None] = mapped_column(Numeric(6,2), nullable=True)
    total_max: Mapped[float | None] = mapped_column(Numeric(6,2), nullable=True)
    percentage: Mapped[float | None] = mapped_column(Numeric(5,2), nullable=True)
    grade: Mapped[str | None] = mapped_column(String(10), nullable=True)
    grade_point: Mapped[float | None] = mapped_column(Numeric(4,2), nullable=True)
    is_pass: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (UniqueConstraint("exam_id", "student_id", "subject_id", name="uq_subject_result"),)

class ExamResult(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "exam_results"
    exam_id: Mapped[UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    
    total_obtained: Mapped[float | None] = mapped_column(Numeric(8,2), nullable=True)
    total_max: Mapped[float | None] = mapped_column(Numeric(8,2), nullable=True)
    percentage: Mapped[float | None] = mapped_column(Numeric(5,2), nullable=True)
    overall_grade: Mapped[str | None] = mapped_column(String(10), nullable=True)
    gpa: Mapped[float | None] = mapped_column(Numeric(4,2), nullable=True)
    overall_result: Mapped[OverallResult] = mapped_column(SQLEnum(OverallResult), nullable=False)
    
    section_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    class_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False)

    __table_args__ = (UniqueConstraint("exam_id", "student_id", name="uq_overall_result"),)


class ReportPeriod(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "report_periods"
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    grading_system_id: Mapped[UUID] = mapped_column(ForeignKey("grading_systems.id", ondelete="RESTRICT"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    name_local: Mapped[str | None] = mapped_column(String(100), nullable=True)

class ReportPeriodExam(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "report_period_exams"
    period_id: Mapped[UUID] = mapped_column(ForeignKey("report_periods.id", ondelete="CASCADE"), nullable=False)
    exam_id: Mapped[UUID] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    weight_percentage: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)

class ReportCardRemark(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "report_card_remarks"
    period_id: Mapped[UUID] = mapped_column(ForeignKey("report_periods.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    class_teacher_remark: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    principal_remark: Mapped[str | None] = mapped_column(String(1000), nullable=True)

class ReportCardStatus(str, enum.Enum):
    GENERATING = "generating"
    READY = "ready"
    FAILED = "failed"

class ReportCard(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "report_cards"
    period_id: Mapped[UUID] = mapped_column(ForeignKey("report_periods.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ReportCardStatus] = mapped_column(SQLEnum(ReportCardStatus), nullable=False)
    
    file_id: Mapped[UUID | None] = mapped_column(ForeignKey("file_metadata.id", ondelete="SET NULL"), nullable=True)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    verification_token: Mapped[str] = mapped_column(String(64), nullable=False, index=True, unique=True)
    
    generated_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
