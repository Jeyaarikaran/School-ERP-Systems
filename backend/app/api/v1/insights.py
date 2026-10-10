from fastapi import APIRouter

router = APIRouter(prefix="/insights", tags=["Insights"])

@router.get("/at-risk")
async def get_at_risk_students():
    return {"success": True, "data": []}

@router.get("/students/{student_id}/risk")
async def get_student_risk(student_id: str):
    return {"success": True, "data": {}}
