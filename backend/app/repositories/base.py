"""Base repository providing tenant isolation."""

from typing import Generic, TypeVar, Any
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.core.database import Base, TenantMixin

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository for tables WITHOUT tenant scoping (e.g., system tables)."""

    def __init__(self, model: type[ModelType], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def get(self, id: UUID) -> ModelType | None:
        result = await self.db_session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def create(self, **kwargs: Any) -> ModelType:
        obj = self.model(**kwargs)
        self.db_session.add(obj)
        await self.db_session.flush()
        return obj


class TenantRepository(BaseRepository[ModelType]):
    """Tenant-aware repository.
    
    Automatically scopes all queries by `school_id`.
    Fails if `school_id` is missing in the context.
    """

    def __init__(self, model: type[ModelType], db_session: AsyncSession, school_id: UUID):
        if not issubclass(model, TenantMixin):
            raise TypeError(f"Model {model.__name__} must inherit from TenantMixin")
        if not school_id:
            raise ValueError("school_id is required for TenantRepository")
            
        super().__init__(model, db_session)
        self.school_id = school_id

    def _scope(self, stmt: Any) -> Any:
        return stmt.where(self.model.school_id == self.school_id)

    async def get(self, id: UUID) -> ModelType | None:
        stmt = self._scope(select(self.model).where(self.model.id == id))
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs: Any) -> ModelType:
        # Override school_id to guarantee tenant safety
        kwargs["school_id"] = self.school_id
        return await super().create(**kwargs)

    async def update(self, id: UUID, **kwargs: Any) -> ModelType | None:
        stmt = (
            update(self.model)
            .where(self.model.id == id, self.model.school_id == self.school_id)
            .values(**kwargs)
            .returning(self.model)
        )
        result = await self.db_session.execute(stmt)
        await self.db_session.flush()
        return result.scalar_one_or_none()

    async def delete(self, id: UUID) -> bool:
        stmt = delete(self.model).where(self.model.id == id, self.model.school_id == self.school_id)
        result = await self.db_session.execute(stmt)
        await self.db_session.flush()
        return result.rowcount > 0
