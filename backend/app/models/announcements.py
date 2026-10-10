import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Index, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    category = Column(String, nullable=False) # notice, circular, event, holiday, emergency
    priority = Column(String, nullable=False, default="normal")
    status = Column(String, nullable=False, default="draft") # draft, pending_approval, scheduled, published, archived
    publish_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    requires_acknowledgement = Column(Boolean, nullable=False, default=False)
    
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    audiences = Column(JSONB, nullable=False, default=list) # [{type: 'role', value: 'student'}, {type: 'section', value: 'uuid'}]
    attachments = Column(JSONB, nullable=False, default=list)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index("ix_announcements_tenant_status", "tenant_id", "status"),
    )

class AnnouncementRecipient(Base):
    __tablename__ = "announcement_recipients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    announcement_id = Column(UUID(as_uuid=True), ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    delivered_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "announcement_id", "user_id", name="uq_announcement_recipients"),
        Index("ix_announcement_recipients_user", "tenant_id", "user_id"),
    )
