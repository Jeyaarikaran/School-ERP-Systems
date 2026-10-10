import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, ForeignKey, DateTime, Date, Boolean, Index, UniqueConstraint, func, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base

class LeaveType(Base):
    __tablename__ = "leave_types"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    applies_to = Column(String, nullable=False) # student, staff
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", "applies_to", name="uq_leave_types_name"),
    )

class LeaveEntitlement(Base):
    __tablename__ = "leave_entitlements"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    leave_type_id = Column(UUID(as_uuid=True), ForeignKey("leave_types.id", ondelete="CASCADE"), nullable=False)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    days_allotted = Column(Numeric(5, 1), nullable=False) # 0.5 granularity
    
    __table_args__ = (
        UniqueConstraint("staff_id", "leave_type_id", "academic_year_id", name="uq_leave_entitlements"),
    )

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    applicant_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject_type = Column(String, nullable=False) # student, staff
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=True)
    leave_type_id = Column(UUID(as_uuid=True), ForeignKey("leave_types.id"), nullable=False)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_half = Column(String, nullable=True) # first_half, second_half
    end_half = Column(String, nullable=True)
    days_count = Column(Numeric(5, 1), nullable=False) # Computed by server
    
    reason = Column(String, nullable=False)
    attachment_url = Column(String, nullable=True)
    
    status = Column(String, nullable=False, default="pending") # pending, approved, rejected, cancelled
    decided_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    decision_note = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index("ix_leave_requests_tenant_status", "tenant_id", "status"),
        Index("ix_leave_requests_student", "student_id"),
        Index("ix_leave_requests_staff", "staff_id"),
    )

class LeaveApproval(Base):
    __tablename__ = "leave_approvals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    request_id = Column(UUID(as_uuid=True), ForeignKey("leave_requests.id", ondelete="CASCADE"), nullable=False)
    step_no = Column(Integer, nullable=False, default=1)
    approver_role = Column(String, nullable=False)
    approver_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status = Column(String, nullable=False)
    decided_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    note = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
