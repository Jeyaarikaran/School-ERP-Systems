from fastapi import APIRouter

router = APIRouter(prefix="/dashboards", tags=["Dashboards"])

@router.get("/me")
async def get_my_dashboard():
    return {"success": True, "data": []}

@router.get("/widgets/{key}")
async def get_widget(key: str):
    return {"success": True, "data": {}}
