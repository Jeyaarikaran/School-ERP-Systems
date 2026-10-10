"""Academic structure Pydantic schemas."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional
from app.models.academic import AcademicYearStatus, SubjectType


class AcademicYearCreate(BaseModel):
    name: str = Field(..., max_length=50)
    start_date: date
    end_date: date


class AcademicYearUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[AcademicYearStatus] = None


class AcademicYearResponse(BaseModel):
    id: UUID
    school_id: UUID
    name: str
    start_date: date
    end_date: date
    status: AcademicYearStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ClassLevelCreate(BaseModel):
    name: str = Field(..., max_length=50)
    level: int
    display_order: int = 0


class ClassLevelUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    level: Optional[int] = None
    display_order: Optional[int] = None


class ClassLevelResponse(BaseModel):
    id: UUID
    school_id: UUID
    name: str
    level: int
    display_order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SectionCreate(BaseModel):
    class_id: UUID
    academic_year_id: UUID
    name: str = Field(..., max_length=20)
    capacity: int = 40
    class_teacher_id: Optional[UUID] = None
    room_id: Optional[UUID] = None


class SectionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=20)
    capacity: Optional[int] = None
    class_teacher_id: Optional[UUID] = None
    room_id: Optional[UUID] = None


class SectionResponse(BaseModel):
    id: UUID
    school_id: UUID
    class_id: UUID
    academic_year_id: UUID
    name: str
    capacity: int
    class_teacher_id: Optional[UUID]
    room_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubjectCreate(BaseModel):
    code: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    name_local: Optional[str] = Field(None, max_length=100)
    type: SubjectType = SubjectType.CORE


class SubjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    name_local: Optional[str] = Field(None, max_length=100)
    type: Optional[SubjectType] = None


class SubjectResponse(BaseModel):
    id: UUID
    school_id: UUID
    code: str
    name: str
    name_local: Optional[str]
    type: SubjectType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ClassSubjectCreate(BaseModel):
    class_id: UUID
    subject_id: UUID
    academic_year_id: UUID
    is_mandatory: bool = True
    weekly_periods: Optional[int] = None


class ClassSubjectUpdate(BaseModel):
    is_mandatory: Optional[bool] = None
    weekly_periods: Optional[int] = None


class ClassSubjectResponse(BaseModel):
    id: UUID
    school_id: UUID
    class_id: UUID
    subject_id: UUID
    academic_year_id: UUID
    is_mandatory: bool
    weekly_periods: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportPeriodCreate(BaseModel):
    academic_year_id: UUID
    grading_system_id: UUID
    name: str = Field(..., max_length=100)
    name_local: Optional[str] = Field(None, max_length=100)


class ReportPeriodUpdate(BaseModel):
    grading_system_id: Optional[UUID] = None
    name: Optional[str] = Field(None, max_length=100)
    name_local: Optional[str] = Field(None, max_length=100)


class ReportPeriodResponse(BaseModel):
    id: UUID
    school_id: UUID
    academic_year_id: UUID
    grading_system_id: UUID
    name: str
    name_local: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
