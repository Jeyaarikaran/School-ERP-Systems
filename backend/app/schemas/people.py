"""People Pydantic Schemas."""

from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from app.models.people import StudentStatus, EnrollmentStatus, StaffStatus


# --- STUDENT ---

class StudentCreate(BaseModel):
    admission_no: str = Field(..., max_length=50)
    full_name: str = Field(..., max_length=150)
    name_local: Optional[str] = Field(None, max_length=150)
    date_of_birth: date
    gender: str = Field(..., max_length=20)
    blood_group: Optional[str] = Field(None, max_length=10)
    address: Optional[Dict[str, Any]] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    emergency_contact: Optional[Dict[str, Any]] = None
    admission_date: date
    previous_school: Optional[str] = Field(None, max_length=255)
    branch_id: Optional[UUID] = None


class StudentUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=150)
    name_local: Optional[str] = Field(None, max_length=150)
    blood_group: Optional[str] = Field(None, max_length=10)
    address: Optional[Dict[str, Any]] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    emergency_contact: Optional[Dict[str, Any]] = None
    status: Optional[StudentStatus] = None
    branch_id: Optional[UUID] = None


class StudentResponse(BaseModel):
    id: UUID
    school_id: UUID
    user_id: Optional[UUID]
    admission_no: str
    full_name: str
    name_local: Optional[str]
    date_of_birth: date
    gender: str
    blood_group: Optional[str]
    address: Optional[Dict[str, Any]]
    phone: Optional[str]
    email: Optional[EmailStr]
    emergency_contact: Optional[Dict[str, Any]]
    photo_file_id: Optional[UUID]
    admission_date: date
    previous_school: Optional[str]
    status: StudentStatus
    branch_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- GUARDIAN ---

class GuardianCreate(BaseModel):
    full_name: str = Field(..., max_length=150)
    phone: str = Field(..., max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[Dict[str, Any]] = None


class GuardianUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[Dict[str, Any]] = None


class GuardianResponse(BaseModel):
    id: UUID
    school_id: UUID
    user_id: Optional[UUID]
    full_name: str
    phone: str
    email: Optional[EmailStr]
    address: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentGuardianCreate(BaseModel):
    student_id: UUID
    guardian_id: UUID
    relationship: str = Field(..., max_length=50)
    is_primary: bool = False
    is_emergency_contact: bool = False
    can_pickup: bool = False
    is_financial_responsible: bool = False


# --- ENROLLMENT ---

class EnrollmentCreate(BaseModel):
    student_id: UUID
    academic_year_id: UUID
    class_id: UUID
    section_id: UUID
    branch_id: Optional[UUID] = None
    roll_no: Optional[int] = None
    start_date: date


class EnrollmentUpdate(BaseModel):
    section_id: Optional[UUID] = None
    roll_no: Optional[int] = None
    status: Optional[EnrollmentStatus] = None
    end_date: Optional[date] = None


class EnrollmentResponse(BaseModel):
    id: UUID
    school_id: UUID
    student_id: UUID
    academic_year_id: UUID
    class_id: UUID
    section_id: UUID
    branch_id: Optional[UUID]
    roll_no: Optional[int]
    status: EnrollmentStatus
    start_date: date
    end_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- STAFF & TEACHER ---

class StaffCreate(BaseModel):
    employee_code: str = Field(..., max_length=50)
    staff_type: str = Field(..., max_length=50)
    full_name: str = Field(..., max_length=150)
    designation: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    joining_date: date
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    branch_id: Optional[UUID] = None


class StaffUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=150)
    designation: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    status: Optional[StaffStatus] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    branch_id: Optional[UUID] = None


class StaffResponse(BaseModel):
    id: UUID
    school_id: UUID
    user_id: Optional[UUID]
    employee_code: str
    staff_type: str
    full_name: str
    designation: Optional[str]
    department: Optional[str]
    joining_date: date
    status: StaffStatus
    phone: Optional[str]
    email: Optional[EmailStr]
    branch_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TeacherCreate(BaseModel):
    staff_id: UUID
    specialization: Optional[str] = Field(None, max_length=255)
    qualification: Optional[str] = Field(None, max_length=255)
    max_weekly_periods: Optional[int] = None


class TeacherResponse(BaseModel):
    id: UUID
    school_id: UUID
    staff_id: UUID
    specialization: Optional[str]
    qualification: Optional[str]
    max_weekly_periods: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TeacherAssignmentCreate(BaseModel):
    teacher_id: UUID
    section_id: UUID
    subject_id: UUID
    academic_year_id: UUID


class TeacherAssignmentResponse(BaseModel):
    id: UUID
    school_id: UUID
    teacher_id: UUID
    section_id: UUID
    subject_id: UUID
    academic_year_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
