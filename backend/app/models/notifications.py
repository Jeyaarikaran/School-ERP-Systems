import uuid
from datetime import datetime, timezone
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Boolean, Index, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    key = Column(String, nullable=False)
    category = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    locale = Column(String, nullable=False, default="en")
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    variables_schema = Column(JSONB, nullable=False, default=dict)
    version = Column(Integer, nullable=False, default=1)
    is_system = Column(Boolean, nullable=False, default=False)
    dlt_template_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "key", "channel", "locale", name="uq_notification_templates_key_channel"),
        Index("ix_notification_templates_tenant_id", "tenant_id"),
    )

class NotificationRule(Base):
    __tablename__ = "notification_rules"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    channels = Column(JSONB, nullable=False, default=list)
    timing_preference = Column(String, nullable=False, default="immediate")
    priority = Column(String, nullable=False, default="normal")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "event_type", name="uq_notification_rules_tenant_event"),
        Index("ix_notification_rules_tenant_id", "tenant_id"),
    )

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(String, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    data = Column(JSONB, nullable=True) # Deep link target and ids
    priority = Column(String, nullable=False, default="normal")
    source_event_id = Column(UUID(as_uuid=True), nullable=True) # Points to outbox event if applicable
    dedupe_key = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    archived_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "user_id", "dedupe_key", name="uq_notifications_dedupe"),
        Index("ix_notifications_tenant_user_created", "tenant_id", "user_id", "created_at"),
    )

class NotificationDelivery(Base):
    __tablename__ = "notification_deliveries"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    notification_id = Column(UUID(as_uuid=True), ForeignKey("notifications.id", ondelete="CASCADE"), nullable=False)
    channel = Column(String, nullable=False) # push, email, sms, in_app
    provider = Column(String, nullable=True)
    status = Column(String, nullable=False, default="queued") # queued, sending, sent, delivered, failed, skipped, suppressed
    attempts = Column(Integer, nullable=False, default=0)
    provider_message_id = Column(String, nullable=True)
    error_code = Column(String, nullable=True)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index("ix_notification_deliveries_tenant_notification", "tenant_id", "notification_id"),
        Index("ix_notification_deliveries_status", "status"),
    )

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "user_id", "category", "channel", name="uq_notification_prefs"),
        Index("ix_notification_prefs_user", "tenant_id", "user_id"),
    )

class DeviceToken(Base):
    __tablename__ = "device_tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device_id = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    fcm_token = Column(String, nullable=False, unique=True)
    app_version = Column(String, nullable=True)
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, nullable=False, default="active") # active, invalid
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "user_id", "device_id", name="uq_device_tokens"),
        Index("ix_device_tokens_tenant_user", "tenant_id", "user_id"),
    )

class Suppression(Base):
    __tablename__ = "suppressions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    target = Column(String, nullable=False) # email address or phone number
    channel = Column(String, nullable=False) # email or sms
    reason = Column(String, nullable=False) # bounce, complaint, opt-out, invalid
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "target", "channel", name="uq_suppressions_target"),
    )

class MessagingUsage(Base):
    __tablename__ = "messaging_usage"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    channel = Column(String, nullable=False)
    year_month = Column(String, nullable=False) # YYYY-MM
    count = Column(Integer, nullable=False, default=0)
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "channel", "year_month", name="uq_messaging_usage"),
    )
