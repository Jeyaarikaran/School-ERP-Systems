import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_student_unauthorized(client: AsyncClient):
    response = await client.post("/api/v1/people/students", json={
        "admission_no": "STU001",
        "full_name": "John Doe",
        "date_of_birth": "2010-01-01",
        "gender": "male",
        "admission_date": "2025-01-01"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_tenant_isolation_student(client: AsyncClient, school_a_token: str, school_b_token: str):
    # School A creates a student
    resp_a = await client.post("/api/v1/people/students", json={
        "admission_no": "STU001",
        "full_name": "School A Student",
        "date_of_birth": "2010-01-01",
        "gender": "male",
        "admission_date": "2025-01-01"
    }, headers={"Authorization": f"Bearer {school_a_token}"})
    if resp_a.status_code != 200:
        print(f"DEBUG resp_a: {resp_a.text}")
    assert resp_a.status_code == 200
    
    # School B lists students
    resp_b = await client.get("/api/v1/people/students", headers={"Authorization": f"Bearer {school_b_token}"})
    if resp_b.status_code != 200:
        print(f"DEBUG resp_b: {resp_b.text}")
    assert resp_b.status_code == 200
    data_b = resp_b.json()["data"]
    
    # School B should not see School A's student
    assert len(data_b) == 0

@pytest.mark.asyncio
async def test_parent_idor_prevention(client: AsyncClient, parent_a_token: str, parent_b_id: str):
    # Parent A attempts to view Parent B's children
    resp = await client.get(f"/api/v1/people/parents/{parent_b_id}/children", headers={"Authorization": f"Bearer {parent_a_token}"})
    # Should be blocked
    assert resp.status_code == 403
