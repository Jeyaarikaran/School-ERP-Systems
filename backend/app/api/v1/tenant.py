"""Tenant API Routes (Schools, Settings, Branches)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.database import get_db_session
from app.core.repository import TenantRepository, BaseRepository
from app.core.responses import SuccessResponse, ResponseMeta, PaginationMeta
from app.permissions.dependencies import require_permission
from app.models.tenant import School, SchoolSettings, Branch
from app.schemas.tenant import (
    SchoolCreate, SchoolUpdate, SchoolResponse,
    SchoolSettingsUpdate, SchoolSettingsResponse,
    BranchCreate, BranchUpdate, BranchResponse
)

router = APIRouter(tags=["Tenant"])


@router.get("/schools/{school_id}", response_model=SuccessResponse[SchoolResponse])
async def get_school(
    school_id: UUID,
    auth_ctx: dict = Depends(require_permission("school.view")),
    db: AsyncSession = Depends(get_db_session)
):
    if str(school_id) != str(auth_ctx["school_id"]) and "super_admin" not in auth_ctx.get("roles", []):
        raise HTTPException(status_code=403, detail="Cross-tenant access forbidden.")
        
    repo = BaseRepository(School, db)
    school = await repo.get(school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
        
    return SuccessResponse(data=SchoolResponse.model_validate(school))


@router.get("/school-settings", response_model=SuccessResponse[SchoolSettingsResponse])
async def get_school_settings(
    auth_ctx: dict = Depends(require_permission("school_settings.view")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = auth_ctx["school_id"]
    if not school_id:
        raise HTTPException(status_code=403, detail="Platform users do not have school settings.")
        
    stmt = select(SchoolSettings).where(SchoolSettings.school_id == str(school_id))
    result = await db.execute(stmt)
    settings = result.scalars().first()
    
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
        
    return SuccessResponse(data=SchoolSettingsResponse.model_validate(settings))


@router.get("/branches", response_model=SuccessResponse[List[BranchResponse]])
async def list_branches(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    auth_ctx: dict = Depends(require_permission("branch.view")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = auth_ctx["school_id"]
    if not school_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    repo = TenantRepository(Branch, db, UUID(school_id))
    skip = (page - 1) * limit
    branches = await repo.get_all(skip=skip, limit=limit)
    
    return SuccessResponse(
        data=[BranchResponse.model_validate(b) for b in branches],
        meta=ResponseMeta(pagination=PaginationMeta(page=page, limit=limit, total=len(branches)+skip, total_pages=1))
    )


@router.post("/branches", response_model=SuccessResponse[BranchResponse])
async def create_branch(
    payload: BranchCreate,
    auth_ctx: dict = Depends(require_permission("branch.create")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = auth_ctx["school_id"]
    repo = TenantRepository(Branch, db, UUID(school_id))
    
    # Simple uniqueness check could be handled by DB constraint catching
    branch = await repo.create(payload.model_dump())
    return SuccessResponse(data=BranchResponse.model_validate(branch))
