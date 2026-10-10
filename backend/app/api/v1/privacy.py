from fastapi import APIRouter

router = APIRouter(prefix="/privacy", tags=["Privacy"])

@router.get("/me")
async def get_my_privacy_settings():
    return {"success": True, "data": {}}

@router.get("/requests")
async def list_data_requests():
    return {"success": True, "data": []}
