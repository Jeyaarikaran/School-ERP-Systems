import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, ForeignKey, DateTime, Date, Boolean, Index, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base

class SubstitutionNeed(Base):
    __tablename__ = "substitution_needs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    timetable_entry_id = Column(UUID(as_uuid=True), ForeignKey("timetable_entries.id", ondelete="CASCADE"), nullable=True) # None for manual entry
    section_id = Column(UUID(as_uuid=True), ForeignKey("sections.id", ondelete="CASCADE"), nullable=True)
    period_id = Column(UUID(as_uuid=True), ForeignKey("bell_schedule_periods.id", ondelete="CASCADE"), nullable=True)
    original_teacher_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    leave_request_id = Column(UUID(as_uuid=True), ForeignKey("leave_requests.id", ondelete="SET NULL"), nullable=True)
    status = Column(String, nullable=False, default="needed") # needed, assigned, covered_cancelled
    reason = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index("ix_substitution_needs_tenant_date", "tenant_id", "date"),
    )

class TimetableSubstitution(Base):
    __tablename__ = "timetable_substitutions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    need_id = Column(UUID(as_uuid=True), ForeignKey("substitution_needs.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    substitute_teacher_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False, default="assigned") # assigned, confirmed, declined, cancelled
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index("ix_timetable_substitutions_substitute_date", "tenant_id", "substitute_teacher_id", "date"),
    )
