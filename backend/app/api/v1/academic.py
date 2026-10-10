"""Academic API Routes (Years, Classes, Sections, Subjects)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.core.database import get_db_session
from app.core.responses import SuccessResponse, ResponseMeta, PaginationMeta
from app.permissions.dependencies import require_permission
from app.schemas.academic import (
    AcademicYearCreate, AcademicYearResponse,
    ClassLevelCreate, ClassLevelResponse,
    SectionCreate, SectionResponse,
    SubjectCreate, SubjectResponse,
    ClassSubjectCreate, ClassSubjectResponse
)
from app.services.academic import AcademicService
from app.models.academic import AcademicYear, ClassLevel, Section, Subject, ClassSubject

router = APIRouter(tags=["Academics"])


@router.post("/academic-years", response_model=SuccessResponse[AcademicYearResponse])
async def create_academic_year(
    payload: AcademicYearCreate,
    auth_ctx: dict = Depends(require_permission("academic_year.create")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = UUID(auth_ctx["school_id"])
    svc = AcademicService(db, school_id)
    try:
        ay = await svc.create_academic_year(payload.model_dump())
        return SuccessResponse(data=AcademicYearResponse.model_validate(ay))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/academic-years", response_model=SuccessResponse[List[AcademicYearResponse]])
async def list_academic_years(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    auth_ctx: dict = Depends(require_permission("academic_year.view")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = UUID(auth_ctx["school_id"])
    svc = AcademicService(db, school_id)
    skip = (page - 1) * limit
    results = await svc.year_repo.get_all(skip=skip, limit=limit)
    return SuccessResponse(
        data=[AcademicYearResponse.model_validate(x) for x in results],
        meta=ResponseMeta(pagination=PaginationMeta(page=page, limit=limit, total=len(results)+skip, total_pages=1))
    )


@router.post("/classes", response_model=SuccessResponse[ClassLevelResponse])
async def create_class(
    payload: ClassLevelCreate,
    auth_ctx: dict = Depends(require_permission("class.create")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = UUID(auth_ctx["school_id"])
    svc = AcademicService(db, school_id)
    try:
        cls = await svc.create_class_level(payload.model_dump())
        return SuccessResponse(data=ClassLevelResponse.model_validate(cls))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/classes", response_model=SuccessResponse[List[ClassLevelResponse]])
async def list_classes(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    auth_ctx: dict = Depends(require_permission("class.view")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = UUID(auth_ctx["school_id"])
    svc = AcademicService(db, school_id)
    skip = (page - 1) * limit
    results = await svc.class_repo.get_all(skip=skip, limit=limit)
    return SuccessResponse(
        data=[ClassLevelResponse.model_validate(x) for x in results],
        meta=ResponseMeta(pagination=PaginationMeta(page=page, limit=limit, total=len(results)+skip, total_pages=1))
    )


@router.post("/sections", response_model=SuccessResponse[SectionResponse])
async def create_section(
    payload: SectionCreate,
    auth_ctx: dict = Depends(require_permission("section.create")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = UUID(auth_ctx["school_id"])
    svc = AcademicService(db, school_id)
    try:
        sec = await svc.create_section(payload.model_dump())
        return SuccessResponse(data=SectionResponse.model_validate(sec))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sections", response_model=SuccessResponse[List[SectionResponse]])
async def list_sections(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    auth_ctx: dict = Depends(require_permission("section.view")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = UUID(auth_ctx["school_id"])
    svc = AcademicService(db, school_id)
    skip = (page - 1) * limit
    results = await svc.section_repo.get_all(skip=skip, limit=limit)
    return SuccessResponse(
        data=[SectionResponse.model_validate(x) for x in results],
        meta=ResponseMeta(pagination=PaginationMeta(page=page, limit=limit, total=len(results)+skip, total_pages=1))
    )


@router.post("/subjects", response_model=SuccessResponse[SubjectResponse])
async def create_subject(
    payload: SubjectCreate,
    auth_ctx: dict = Depends(require_permission("subject.create")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = UUID(auth_ctx["school_id"])
    svc = AcademicService(db, school_id)
    sub = await svc.subject_repo.create(payload.model_dump())
    return SuccessResponse(data=SubjectResponse.model_validate(sub))


@router.get("/subjects", response_model=SuccessResponse[List[SubjectResponse]])
async def list_subjects(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    auth_ctx: dict = Depends(require_permission("subject.view")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = UUID(auth_ctx["school_id"])
    svc = AcademicService(db, school_id)
    skip = (page - 1) * limit
    results = await svc.subject_repo.get_all(skip=skip, limit=limit)
    return SuccessResponse(
        data=[SubjectResponse.model_validate(x) for x in results],
        meta=ResponseMeta(pagination=PaginationMeta(page=page, limit=limit, total=len(results)+skip, total_pages=1))
    )


@router.post("/class-subjects", response_model=SuccessResponse[ClassSubjectResponse])
async def create_class_subject(
    payload: ClassSubjectCreate,
    auth_ctx: dict = Depends(require_permission("class_subject.create")),
    db: AsyncSession = Depends(get_db_session)
):
    school_id = UUID(auth_ctx["school_id"])
    svc = AcademicService(db, school_id)
    try:
        cs = await svc.create_class_subject(payload.model_dump())
        return SuccessResponse(data=ClassSubjectResponse.model_validate(cs))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
