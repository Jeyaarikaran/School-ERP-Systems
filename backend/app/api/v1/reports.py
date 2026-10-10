from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/catalog")
async def get_report_catalog():
    return {"success": True, "data": []}

@router.post("/jobs")
async def create_report_job():
    return {"success": True, "data": {}}

@router.get("/jobs/{job_id}")
async def get_report_job(job_id: str):
    return {"success": True, "data": {}}
