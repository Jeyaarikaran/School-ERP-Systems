"""Attendance Pydantic schemas."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional


class AttendanceRecordInput(BaseModel):
    student_id: UUID
    status: str
    remarks: Optional[str] = None
    arrival_time: Optional[str] = None


class AttendanceSubmitRequest(BaseModel):
    base_version: int = 0
    records: list[AttendanceRecordInput]


class AttendanceRecordResponse(BaseModel):
    student_id: UUID
    status: str
    remarks: str | None
    record_version: int

    class Config:
        from_attributes = True


class AttendanceSessionResponse(BaseModel):
    id: UUID
    section_id: UUID
    attendance_date: date
    state: str
    version: int
    submitted_by_id: UUID | None
    submitted_at: datetime | None

    class Config:
        from_attributes = True


class SyncOpRequest(BaseModel):
    client_op_id: str
    section_id: UUID
    attendance_date: date
    base_version: int
    records: list[AttendanceRecordInput]
    client_created_at: datetime


class SyncBatchRequest(BaseModel):
    device_id: str
    ops: list[SyncOpRequest]


class RecordResult(BaseModel):
    student_id: UUID
    result: str  # applied, unchanged, conflict, rejected
    action: str
    server_value: Optional[dict] = None


class SyncOpResult(BaseModel):
    client_op_id: str
    status: str  # applied, partially_applied, duplicate, conflict, rejected
    session_version: Optional[int] = None
    record_results: list[RecordResult]
    code: Optional[str] = None


class SyncBatchResponse(BaseModel):
    results: list[SyncOpResult]
