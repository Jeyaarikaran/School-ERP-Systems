import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_academic_year_unauthorized(client: AsyncClient):
    response = await client.post("/api/v1/academics/academic-years", json={
        "name": "2025-2026",
        "start_date": "2025-04-01",
        "end_date": "2026-03-31"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_branch_unauthorized(client: AsyncClient):
    response = await client.post("/api/v1/tenant/branches", json={
        "name": "Main Branch",
        "code": "MAIN"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_cross_tenant_school_access(client: AsyncClient, school_a_token: str, school_b_id: str):
    response = await client.get(f"/api/v1/tenant/schools/{school_b_id}", headers={"Authorization": f"Bearer {school_a_token}"})
    assert response.status_code == 403

# Tests assuming we have a mock user fixture yielding a token for a school admin
@pytest.mark.asyncio
async def test_create_academic_year_valid(client: AsyncClient, school_admin_token: str):
    response = await client.post("/api/v1/academics/academic-years", json={
        "name": "2025-2026",
        "start_date": "2025-04-01",
        "end_date": "2026-03-31"
    }, headers={"Authorization": f"Bearer {school_admin_token}"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "2025-2026"

@pytest.mark.asyncio
async def test_create_academic_year_invalid_dates(client: AsyncClient, school_admin_token: str):
    response = await client.post("/api/v1/academics/academic-years", json={
        "name": "2025-2026",
        "start_date": "2026-03-31",
        "end_date": "2025-04-01"
    }, headers={"Authorization": f"Bearer {school_admin_token}"})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_tenant_isolation_classes(client: AsyncClient, school_a_token: str, school_b_token: str):
    # School A creates a class
    resp_a = await client.post("/api/v1/academics/classes", json={
        "name": "Grade 10",
        "level": 10
    }, headers={"Authorization": f"Bearer {school_a_token}"})
    assert resp_a.status_code == 200
    
    # School B lists classes
    resp_b = await client.get("/api/v1/academics/classes", headers={"Authorization": f"Bearer {school_b_token}"})
    assert resp_b.status_code == 200
    data_b = resp_b.json()["data"]
    
    # School B should not see School A's class
    assert len(data_b) == 0
