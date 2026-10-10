"""Database engine, async session factory, and base model."""

from collections.abc import AsyncIterator
from datetime import datetime

from sqlalchemy import MetaData, func, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from uuid import UUID, uuid4

from app.core.config import settings

# Naming convention for constraints (Alembic auto-generates names)
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,
    echo=settings.app_debug and settings.app_env == "development",
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency that yields an async DB session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    metadata = MetaData(naming_convention=convention)


class UUIDPrimaryKeyMixin:
    """Mixin that adds a UUID primary key."""

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps.

    These are DB-owned — never set by clients.
    """

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class TenantMixin:
    """Mixin that adds school_id for tenant-scoped tables."""

    school_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )


class SoftDeleteMixin:
    """Mixin for soft-deletable entities."""

    deleted_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
        default=None,
    )
