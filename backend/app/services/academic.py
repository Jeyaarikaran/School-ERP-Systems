"""Academic Service layer."""

from uuid import UUID
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import Optional

from app.models.academic import AcademicYear, ClassLevel, Section, Subject, ClassSubject, AcademicYearStatus
from app.core.repository import TenantRepository


class AcademicService:
    def __init__(self, db: AsyncSession, school_id: UUID):
        self.db = db
        self.school_id = school_id
        self.year_repo = TenantRepository(AcademicYear, db, school_id)
        self.class_repo = TenantRepository(ClassLevel, db, school_id)
        self.section_repo = TenantRepository(Section, db, school_id)
        self.subject_repo = TenantRepository(Subject, db, school_id)
        self.class_subject_repo = TenantRepository(ClassSubject, db, school_id)

    async def create_academic_year(self, data: dict) -> AcademicYear:
        start_date = data["start_date"]
        end_date = data["end_date"]
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")
            
        # Check overlaps
        stmt = select(AcademicYear).where(
            AcademicYear.school_id == self.school_id,
            or_(
                and_(AcademicYear.start_date <= end_date, AcademicYear.end_date >= start_date)
            )
        )
        existing = await self.db.execute(stmt)
        if existing.scalars().first():
            raise ValueError("Dates overlap with an existing academic year")
            
        return await self.year_repo.create(data)

    async def create_class_level(self, data: dict) -> ClassLevel:
        stmt = select(ClassLevel).where(
            ClassLevel.school_id == self.school_id,
            ClassLevel.name == data["name"]
        )
        existing = await self.db.execute(stmt)
        if existing.scalars().first():
            raise ValueError("Class name already exists")
            
        return await self.class_repo.create(data)

    async def create_section(self, data: dict) -> Section:
        stmt = select(Section).where(
            Section.school_id == self.school_id,
            Section.class_id == data["class_id"],
            Section.academic_year_id == data["academic_year_id"],
            Section.name == data["name"]
        )
        existing = await self.db.execute(stmt)
        if existing.scalars().first():
            raise ValueError("Section already exists for this class and academic year")
            
        return await self.section_repo.create(data)

    async def create_class_subject(self, data: dict) -> ClassSubject:
        stmt = select(ClassSubject).where(
            ClassSubject.school_id == self.school_id,
            ClassSubject.class_id == data["class_id"],
            ClassSubject.subject_id == data["subject_id"],
            ClassSubject.academic_year_id == data["academic_year_id"]
        )
        existing = await self.db.execute(stmt)
        if existing.scalars().first():
            raise ValueError("This subject is already mapped to this class for this academic year")
            
        return await self.class_subject_repo.create(data)
