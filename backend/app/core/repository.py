from typing import Generic, TypeVar, Type, Any, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from uuid import UUID

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    """
    Base Repository for GLOBAL models (e.g., Schools, SystemSettings).
    Does NOT enforce tenant isolation. Use cautiously.
    """
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj


class TenantRepository(BaseRepository[ModelType]):
    """
    Strict Tenant-Scoped Repository.
    Enforces ADR-003 Multi-tenancy by strictly applying `WHERE school_id = ctx`
    to ALL queries and stamping `school_id` on all INSERTS.
    """
    def __init__(self, model: Type[ModelType], db: AsyncSession, school_id: UUID):
        super().__init__(model, db)
        self.school_id = school_id

    def _apply_tenant_filter(self, stmt):
        """Internal helper to always append the tenant scope."""
        return stmt.where(self.model.school_id == self.school_id)

    async def get(self, id: Any) -> Optional[ModelType]:
        """Fetch a single record, strictly scoped to the tenant."""
        stmt = self._apply_tenant_filter(select(self.model).where(self.model.id == id))
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """Fetch multiple records (Offset Pagination per ADR-008), strictly scoped to the tenant."""
        stmt = self._apply_tenant_filter(select(self.model)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj_in: dict) -> ModelType:
        """Create a record, explicitly injecting the school_id context to prevent leakage."""
        obj_in["school_id"] = self.school_id
        return await super().create(obj_in)

    async def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        """Update a record. Relies on the fact that db_obj was fetched via a tenant-scoped get()."""
        if "school_id" in obj_in and obj_in["school_id"] != self.school_id:
            raise ValueError("Cross-tenant mutation attempt blocked.")
            
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
            
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj
