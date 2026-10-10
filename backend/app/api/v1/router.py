"""API v1 router — aggregates all module routers."""

from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.students import router as students_router
from app.api.v1.attendance import router as attendance_router
from app.api.v1.reports import router as reports_router
from app.api.v1.dashboards import router as dashboards_router
from app.api.v1.insights import router as insights_router
from app.api.v1.privacy import router as privacy_router
from app.api.v1.ai import router as ai_router
from app.api.v1.tenant import router as tenant_router
from app.api.v1.academic import router as academic_router
from app.api.v1.people import router as people_router

api_router = APIRouter()

# Health & readiness (no auth)
api_router.include_router(health_router, tags=["Health"])

# Modules
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(students_router)
api_router.include_router(attendance_router)
api_router.include_router(reports_router)
api_router.include_router(dashboards_router)
api_router.include_router(insights_router)
api_router.include_router(privacy_router)
api_router.include_router(ai_router)
api_router.include_router(tenant_router, prefix="/tenant", tags=["Tenant"])
api_router.include_router(academic_router, prefix="/academics", tags=["Academics"])
api_router.include_router(people_router, prefix="/people", tags=["People"])

# api_router.include_router(students_router, prefix="/students", tags=["Students"])
# api_router.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
# api_router.include_router(fees_router, prefix="/fees", tags=["Fees"])
# ... etc.
