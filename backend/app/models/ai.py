"""AI models — feature flags, jobs, usage tracking, and human-in-the-loop approvals.

All AI features are strictly opt-in, track usage for billing/quotas,
and require human approval before any output is shown to parents.
"""

from datetime import datetime
from uuid import UUID
import enum

from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Index, Integer, Numeric,
    String, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


# ------------------------------------------------------------------
# AI Feature Configuration
# ------------------------------------------------------------------
class AIFeatureToggle(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Granular toggles for AI features per school."""
    __tablename__ = "ai_feature_toggles"

    feature_key: Mapped[str] = mapped_column(String(50), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    monthly_budget_usd: Mapped[Numeric | None] = mapped_column(Numeric(10, 4), nullable=True)
    provider_override: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model_override: Mapped[str | None] = mapped_column(String(50), nullable=True)

    __table_args__ = (
        UniqueConstraint("school_id", "feature_key", name="uq_ai_feature_toggle"),
    )


# ------------------------------------------------------------------
# AI Jobs and Usage
# ------------------------------------------------------------------
class AIJobStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    QUOTA_EXCEEDED = "quota_exceeded"


class AIJob(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Tracks asynchronous AI requests and their status."""
    __tablename__ = "ai_jobs"

    feature_key: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    requester_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[AIJobStatus] = mapped_column(default=AIJobStatus.QUEUED, nullable=False)
    
    # The payload contains context IDs, not raw PII text when possible
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    
    # The output is stored here temporarily; once approved, it moves to the domain model
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model: Mapped[str | None] = mapped_column(String(50), nullable=True)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cost_usd: Mapped[Numeric] = mapped_column(Numeric(10, 6), default=0, nullable=False)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_ai_jobs_school_status", "school_id", "status"),
    )


class AIUsageLog(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Daily aggregated usage for quota enforcement."""
    __tablename__ = "ai_usage_logs"

    usage_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    feature_key: Mapped[str] = mapped_column(String(50), nullable=False)
    request_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_cost_usd: Mapped[Numeric] = mapped_column(Numeric(10, 6), default=0, nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "usage_date", "feature_key", name="uq_ai_usage_log"),
    )


# ------------------------------------------------------------------
# Human-in-the-loop Drafts
# ------------------------------------------------------------------
class DraftStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISCARDED = "discarded"


class AIDraft(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """AI-generated content waiting for human approval."""
    __tablename__ = "ai_drafts"

    job_id: Mapped[UUID] = mapped_column(ForeignKey("ai_jobs.id", ondelete="CASCADE"), nullable=False, unique=True)
    feature_key: Mapped[str] = mapped_column(String(50), nullable=False)
    target_entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "student"
    target_entity_id: Mapped[UUID] = mapped_column(nullable=False)
    
    # Original AI output and the edited version
    original_content: Mapped[str] = mapped_column(String, nullable=False)
    edited_content: Mapped[str | None] = mapped_column(String, nullable=True)
    
    status: Mapped[DraftStatus] = mapped_column(default=DraftStatus.PENDING, nullable=False)
    
    created_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    decided_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    feedback_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1-5 or -1/1
    feedback_text: Mapped[str | None] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        Index("ix_ai_drafts_target", "target_entity_type", "target_entity_id"),
        Index("ix_ai_drafts_status", "school_id", "status"),
    )
