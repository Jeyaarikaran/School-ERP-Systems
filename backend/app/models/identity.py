"""Identity models: Users, authentication, and sessions."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import String, Boolean, text, JSON, Enum as SQLEnum, ForeignKey, Index, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class UserStatus(str, enum.Enum):
    INVITED = "invited"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """User account representation."""
    __tablename__ = "users"

    school_id: Mapped[UUID | None] = mapped_column(ForeignKey("schools.id"), nullable=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[UserStatus] = mapped_column(SQLEnum(UserStatus), default=UserStatus.INVITED, nullable=False)
    
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    phone_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    must_change_password: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    failed_login_count: Mapped[int] = mapped_column(default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    locale: Mapped[str] = mapped_column(String(10), default="en", nullable=False)

    __table_args__ = (
        Index("ix_users_school_email", "school_id", "email", unique=True, postgresql_where=text("email IS NOT NULL AND school_id IS NOT NULL")),
        Index("ix_users_school_phone", "school_id", "phone", unique=True, postgresql_where=text("phone IS NOT NULL AND school_id IS NOT NULL")),
        Index("ix_users_platform_email", "email", unique=True, postgresql_where=text("email IS NOT NULL AND school_id IS NULL")),
    )

    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")


class UserSession(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Active user session representation."""
    __tablename__ = "user_sessions"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    device_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_reason: Mapped[str | None] = mapped_column(String(100), nullable=True)

    user = relationship("User", back_populates="sessions")
    refresh_tokens = relationship("RefreshToken", back_populates="session", cascade="all, delete-orphan")


class RefreshToken(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Rotating refresh token storage."""
    __tablename__ = "refresh_tokens"

    session_id: Mapped[UUID] = mapped_column(ForeignKey("user_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    family_id: Mapped[UUID] = mapped_column(index=True, nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    session = relationship("UserSession", back_populates="refresh_tokens")


class OTPCode(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """One-time password codes."""
    __tablename__ = "otp_codes"

    phone: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    code_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    attempts: Mapped[int] = mapped_column(default=0, nullable=False)


class TwoFactorSecret(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """TOTP secrets for users."""
    __tablename__ = "two_factor_secrets"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    secret: Mapped[str] = mapped_column(String(255), nullable=False)  # Encrypted at rest
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class TwoFactorRecoveryCode(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Recovery codes for 2FA."""
    __tablename__ = "two_factor_recovery_codes"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    code_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class UserIdentity(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """External identity providers linked to a user (e.g., Google)."""
    __tablename__ = "user_identities"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False) # e.g., google
    provider_subject: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("provider", "provider_subject", name="uq_user_identities_provider_sub"),
    )

