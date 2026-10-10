"""People API Routes (Students, Parents, Teachers, Staff)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from sqlalchemy import select

from app.core.database import get_db_session
from app.core.responses import SuccessResponse, ResponseMeta, PaginationMeta
from app.permissions.dependencies import require_permission
from app.schemas.people import (
    StudentCreate, StudentResponse,
    GuardianCreate, GuardianResponse, StudentGuardianCreate,
    EnrollmentCreate, EnrollmentResponse,
    StaffCreate, StaffResponse,
    TeacherCreate, TeacherResponse,
    TeacherAssignmentCreate, TeacherAssignmentResponse
)
from app.services.people import PeopleService
from app.models.people import StudentGuardian

router = APIRouter(tags=["People"])


@router.post("/students", response_model=SuccessResponse[StudentResponse])
async def create_student(
    payload: StudentCreate,
    auth_ctx: dict = Depends(require_permission("student.create")),
    db: AsyncSession = Depends(get_db_session)
):
    svc = PeopleService(db, UUID(auth_ctx["school_id"]), UUID(auth_ctx.get("user_id")))
    try:
        student = await svc.create_student(payload.model_dump())
        return SuccessResponse(data=StudentResponse.model_validate(student))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/students/bulk-import")
async def bulk_create_students(
    payload: List[StudentCreate],
    auth_ctx: dict = Depends(require_permission("student.create")),
    db: AsyncSession = Depends(get_db_session)
):
    svc = PeopleService(db, UUID(auth_ctx["school_id"]), UUID(auth_ctx.get("user_id")))
    try:
        # Convert models to dicts for bulk import
        data = [p.model_dump() for p in payload]
        result = await svc.bulk_create_students(data)
        return SuccessResponse(data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/students", response_model=SuccessResponse[List[StudentResponse]])
async def list_students(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    auth_ctx: dict = Depends(require_permission("student.view")),
    db: AsyncSession = Depends(get_db_session)
):
    svc = PeopleService(db, UUID(auth_ctx["school_id"]), UUID(auth_ctx.get("user_id")))
    skip = (page - 1) * limit
    results = await svc.student_repo.get_all(skip=skip, limit=limit)
    return SuccessResponse(
        data=[StudentResponse.model_validate(x) for x in results],
        meta=ResponseMeta(pagination=PaginationMeta(page=page, limit=limit, total=len(results)+skip, total_pages=1))
    )


@router.post("/student-enrollments", response_model=SuccessResponse[EnrollmentResponse])
async def enroll_student(
    payload: EnrollmentCreate,
    auth_ctx: dict = Depends(require_permission("enrollment.create")),
    db: AsyncSession = Depends(get_db_session)
):
    svc = PeopleService(db, UUID(auth_ctx["school_id"]))
    try:
        enrollment = await svc.enroll_student(payload.model_dump())
        return SuccessResponse(data=EnrollmentResponse.model_validate(enrollment))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/parents", response_model=SuccessResponse[GuardianResponse])
async def create_parent(
    payload: GuardianCreate,
    auth_ctx: dict = Depends(require_permission("parent.create")),
    db: AsyncSession = Depends(get_db_session)
):
    svc = PeopleService(db, UUID(auth_ctx["school_id"]))
    parent = await svc.guardian_repo.create(payload.model_dump())
    return SuccessResponse(data=GuardianResponse.model_validate(parent))


@router.post("/parents/link", response_model=SuccessResponse[dict])
async def link_parent_child(
    payload: StudentGuardianCreate,
    auth_ctx: dict = Depends(require_permission("parent.update")),
    db: AsyncSession = Depends(get_db_session)
):
    svc = PeopleService(db, UUID(auth_ctx["school_id"]))
    try:
        link = await svc.link_guardian(payload.student_id, payload.guardian_id, payload.model_dump())
        return SuccessResponse(data={"id": link.id, "message": "Linked successfully"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/parents/{parent_id}/children", response_model=SuccessResponse[List[StudentResponse]])
async def get_parent_children(
    parent_id: UUID,
    auth_ctx: dict = Depends(require_permission("parent.view")),
    db: AsyncSession = Depends(get_db_session)
):
    # IDOR Check for parents querying their own children
    if "parent" in auth_ctx.get("roles", []) and str(auth_ctx.get("user_id")) != str(parent_id):
        raise HTTPException(status_code=403, detail="Can only view own children")

    stmt = select(StudentGuardian).where(
        StudentGuardian.school_id == str(auth_ctx["school_id"]),
        StudentGuardian.guardian_id == parent_id
    )
    result = await db.execute(stmt)
    links = result.scalars().all()
    
    svc = PeopleService(db, UUID(auth_ctx["school_id"]))
    children = []
    for link in links:
        child = await svc.student_repo.get(link.student_id)
        if child:
            children.append(child)
            
    return SuccessResponse(data=[StudentResponse.model_validate(c) for c in children])


@router.post("/staff", response_model=SuccessResponse[StaffResponse])
async def create_staff(
    payload: StaffCreate,
    auth_ctx: dict = Depends(require_permission("staff.create")),
    db: AsyncSession = Depends(get_db_session)
):
    svc = PeopleService(db, UUID(auth_ctx["school_id"]))
    staff = await svc.staff_repo.create(payload.model_dump())
    return SuccessResponse(data=StaffResponse.model_validate(staff))


@router.post("/teachers", response_model=SuccessResponse[TeacherResponse])
async def create_teacher(
    payload: TeacherCreate,
    auth_ctx: dict = Depends(require_permission("teacher.create")),
    db: AsyncSession = Depends(get_db_session)
):
    svc = PeopleService(db, UUID(auth_ctx["school_id"]))
    teacher = await svc.teacher_repo.create(payload.model_dump())
    return SuccessResponse(data=TeacherResponse.model_validate(teacher))


@router.post("/teacher-assignments", response_model=SuccessResponse[TeacherAssignmentResponse])
async def assign_teacher(
    payload: TeacherAssignmentCreate,
    auth_ctx: dict = Depends(require_permission("teacher_assignment.create")),
    db: AsyncSession = Depends(get_db_session)
):
    svc = PeopleService(db, UUID(auth_ctx["school_id"]))
    try:
        assignment = await svc.assign_teacher(payload.model_dump())
        return SuccessResponse(data=TeacherAssignmentResponse.model_validate(assignment))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
