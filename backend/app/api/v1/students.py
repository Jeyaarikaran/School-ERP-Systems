from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db_session
from app.core.repository import TenantRepository
from app.models.people import Student
from app.permissions.dependencies import require_permission
from app.core.responses import SuccessResponse, ResponseMeta, PaginationMeta

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("", response_model=SuccessResponse[List[dict]])
async def list_students(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    auth_ctx: dict = Depends(require_permission("students.view")),
    db: AsyncSession = Depends(get_db_session)
):
    """
    List students strictly scoped to the user's tenant.
    Enforces 'students.view' permission and Offset Pagination.
    """
    school_id = auth_ctx["school_id"]
    if not school_id:
        raise HTTPException(status_code=403, detail="Platform users cannot access tenant students directly.")

    # Initialize Tenant-scoped Repository
    student_repo = TenantRepository(Student, db, school_id)
    
    # Calculate skip for offset pagination
    skip = (page - 1) * limit
    
    # Fetch data (the repo applies `WHERE school_id = :school_id` automatically)
    students = await student_repo.get_all(skip=skip, limit=limit)
    
    # In a full implementation, we'd do a count query for `total`, 
    # but we'll mock it for scaffolding to adhere to the strict JSON envelope.
    total = len(students) + skip # Mock
    total_pages = 1 # Mock
    
    return SuccessResponse(
        data=[
            {
                "id": str(s.id),
                "full_name": s.full_name,
                "admission_no": s.admission_no,
                "status": s.status
            } 
            for s in students
        ],
        meta=ResponseMeta(
            pagination=PaginationMeta(
                page=page,
                limit=limit,
                total=total,
                total_pages=total_pages
            )
        )
    )
