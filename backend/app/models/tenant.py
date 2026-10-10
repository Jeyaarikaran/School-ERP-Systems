"""Tenant models: Schools and related settings."""

from sqlalchemy import String, Boolean, JSON, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin
from sqlalchemy.orm import foreign
from sqlalchemy import cast, String


class SchoolStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"


class School(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Platform tenant representation."""
    __tablename__ = "schools"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    status: Mapped[SchoolStatus] = mapped_column(SQLEnum(SchoolStatus), default=SchoolStatus.PENDING, nullable=False)
    domain: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)

    settings = relationship(
        "SchoolSettings",
        back_populates="school",
        uselist=False,
        cascade="all, delete-orphan",
        primaryjoin="foreign(SchoolSettings.school_id) == cast(School.id, String)"
    )


class SchoolSettings(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Tenant configuration."""
    __tablename__ = "school_settings"

    school_id: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata", nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    is_onboarding_complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    features: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    school = relationship(
        "School",
        back_populates="settings",
        primaryjoin="foreign(SchoolSettings.school_id) == cast(School.id, String)"
    )


class SystemSettings(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Global platform configuration."""
    __tablename__ = "system_settings"

    key: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    value: Mapped[dict] = mapped_column(JSON, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

class Branch(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Physical or logical branch of a school."""
    __tablename__ = "branches"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[SchoolStatus] = mapped_column(SQLEnum(SchoolStatus), default=SchoolStatus.ACTIVE, nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "code", name="uq_branch_code_school"),
        UniqueConstraint("school_id", "name", name="uq_branch_name_school"),
    )
