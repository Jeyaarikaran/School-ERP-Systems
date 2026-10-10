from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.permissions.dependencies import require_permission
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db_session),
    # Enforce RBAC using the dependencies built in Phase 2
    _=Depends(require_permission("users.view"))
):
    """List all users in the tenant scope."""
    # Placeholder: fetch from TenantRepository
    return []

