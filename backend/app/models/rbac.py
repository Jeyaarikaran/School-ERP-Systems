"""RBAC models: Roles, permissions, and assignments."""

from uuid import UUID

from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class ScopeType(str, enum.Enum):
    GLOBAL = "GLOBAL"
    SCHOOL = "SCHOOL"
    BRANCH = "BRANCH"
    CLASS = "CLASS"
    SECTION = "SECTION"
    SUBJECT = "SUBJECT"
    ASSIGNED = "ASSIGNED"
    SELF = "SELF"
    CHILD = "CHILD"


class Role(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Role definition (System or Custom per school)."""
    __tablename__ = "roles"

    school_id: Mapped[UUID | None] = mapped_column(ForeignKey("schools.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_role_school_name"),
    )


class Permission(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Global permission catalog (Not tenant-scoped)."""
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    module: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)


class RolePermission(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Mapping of roles to permissions."""
    __tablename__ = "role_permissions"

    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), index=True, nullable=False)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), index=True, nullable=False)
    scope: Mapped[ScopeType] = mapped_column(SQLEnum(ScopeType), default=ScopeType.SCHOOL, nullable=False)

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )


class UserRole(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Mapping of users to roles."""
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), index=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
