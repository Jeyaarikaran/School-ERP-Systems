"""Privacy module models — consents, policies, data requests, retention.

Implements consent management for minors (guardian-granted), policy
acceptance tracking, and data subject request processing with
verification, export, and erasure/anonymization support.
"""

from datetime import date, datetime
from uuid import UUID
import enum

from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Index, Integer,
    String, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


# ------------------------------------------------------------------
# Consents
# ------------------------------------------------------------------
class ConsentPurpose(str, enum.Enum):
    AI_PROCESSING = "ai_processing"
    PHOTO_USAGE = "photo_usage"
    COMMUNICATIONS = "communications"
    ANALYTICS = "analytics"


class Consent(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Records consent for a specific purpose for a data subject.

    For minors (students), consent is granted by a linked guardian.
    Consent history is append-only: withdrawal creates a new row with
    withdrawn_at set; the original row is never modified.
    """
    __tablename__ = "consents"

    subject_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, guardian, staff
    subject_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    purpose: Mapped[ConsentPurpose] = mapped_column(nullable=False)
    granted_by_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    policy_version: Mapped[str] = mapped_column(String(20), nullable=False)
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_consents_subject", "subject_type", "subject_id"),
        Index("ix_consents_active", "school_id", "subject_id", "purpose",
              postgresql_where="withdrawn_at IS NULL"),
    )


# ------------------------------------------------------------------
# Policy documents
# ------------------------------------------------------------------
class PolicyType(str, enum.Enum):
    PRIVACY_POLICY = "privacy_policy"
    TERMS = "terms"
    AI_NOTICE = "ai_notice"


class PolicyDocument(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Versioned policy documents (privacy policy, terms, AI notice)."""
    __tablename__ = "policy_documents"

    policy_type: Mapped[PolicyType] = mapped_column(nullable=False)
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    locale: Mapped[str] = mapped_column(String(5), nullable=False, default="en")  # en, ta
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)  # markdown or plain text
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "policy_type", "version", "locale", name="uq_policy_doc_version_locale"),
        Index("ix_policy_doc_active", "school_id", "policy_type", "is_active"),
    )


class PolicyAcceptance(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Records a user's acceptance of a policy document version."""
    __tablename__ = "policy_acceptances"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    policy_document_id: Mapped[UUID] = mapped_column(ForeignKey("policy_documents.id", ondelete="CASCADE"), nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "policy_document_id", name="uq_policy_acceptance_user_doc"),
    )


# ------------------------------------------------------------------
# Data subject requests (export, correction, erasure)
# ------------------------------------------------------------------
class DataRequestType(str, enum.Enum):
    ACCESS_EXPORT = "access_export"
    CORRECTION = "correction"
    ERASURE = "erasure"


class DataRequestStatus(str, enum.Enum):
    RECEIVED = "received"
    VERIFYING = "verifying"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class DataRequest(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Data subject access / correction / erasure requests."""
    __tablename__ = "data_requests"

    request_type: Mapped[DataRequestType] = mapped_column(nullable=False)
    subject_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, guardian, staff
    subject_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    requested_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[DataRequestStatus] = mapped_column(
        default=DataRequestStatus.RECEIVED, nullable=False
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    handled_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approved_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    result_file_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    result_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # correction fields, erasure report, etc.
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_data_requests_subject", "subject_type", "subject_id"),
        Index("ix_data_requests_status", "school_id", "status"),
    )


# ------------------------------------------------------------------
# Retention registry
# ------------------------------------------------------------------
class RetentionAction(str, enum.Enum):
    DELETE = "delete"
    ANONYMIZE = "anonymize"


class RetentionPolicy(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Registry of data retention rules.

    Not tenant-scoped — these are system-wide defaults.
    Schools can override retention periods via settings.
    """
    __tablename__ = "retention_policies"

    dataset: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)  # e.g. "notifications", "boarding_events"
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    default_retention_days: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[RetentionAction] = mapped_column(nullable=False)
    job_name: Mapped[str] = mapped_column(String(80), nullable=False)
    is_configurable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    legal_basis: Mapped[str | None] = mapped_column(String(255), nullable=True)
