"""People Service layer."""

from uuid import UUID
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import Optional

from app.models.people import (
    Student, Guardian, StudentGuardian, StudentEnrollment, 
    Staff, Teacher, TeacherSubject
)
from app.models.academic import Section, AcademicYear, ClassLevel
from app.core.repository import TenantRepository
from app.services.audit import AuditService


class PeopleService:
    def __init__(self, db: AsyncSession, school_id: UUID, actor_id: UUID | None = None):
        self.db = db
        self.school_id = school_id
        self.actor_id = actor_id
        self.audit = AuditService(db)
        self.student_repo = TenantRepository(Student, db, school_id)
        self.guardian_repo = TenantRepository(Guardian, db, school_id)
        self.enrollment_repo = TenantRepository(StudentEnrollment, db, school_id)
        self.staff_repo = TenantRepository(Staff, db, school_id)
        self.teacher_repo = TenantRepository(Teacher, db, school_id)
        self.assignment_repo = TenantRepository(TeacherSubject, db, school_id)

    async def create_student(self, data: dict) -> Student:
        # Check uniqueness of admission number
        stmt = select(Student).where(
            Student.school_id == self.school_id,
            Student.admission_no == data["admission_no"]
        )
        existing = await self.db.execute(stmt)
        if existing.scalars().first():
            raise ValueError("Admission number already exists")
            
        student = await self.student_repo.create(data)
        await self.audit.record(
            actor_user_id=self.actor_id,
            actor_type="user",
            action="student.created",
            entity_type="student",
            entity_id=str(student.id),
            new_value=data,
            school_id=self.school_id
        )
        return student

    async def bulk_create_students(self, students_data: list[dict]) -> dict:
        """Efficiently create multiple students at once."""
        if not students_data:
            return {"success": 0, "errors": []}
            
        # Bulk check admission numbers
        admission_nos = [s["admission_no"] for s in students_data if "admission_no" in s]
        stmt = select(Student.admission_no).where(
            Student.school_id == self.school_id,
            Student.admission_no.in_(admission_nos)
        )
        existing_nos = set((await self.db.execute(stmt)).scalars().all())
        
        valid_students = []
        errors = []
        
        for idx, row in enumerate(students_data):
            adm_no = row.get("admission_no")
            if adm_no in existing_nos:
                errors.append({"row": idx, "error": f"Admission number {adm_no} exists"})
                continue
            row["school_id"] = self.school_id
            valid_students.append(Student(**row))
            existing_nos.add(adm_no) # Prevent duplicates within the batch itself
            
        if valid_students:
            self.db.add_all(valid_students)
            await self.db.flush()
            
            # Audit log bulk operation
            await self.audit.record(
                actor_user_id=self.actor_id,
                actor_type="user",
                action="student.bulk_created",
                entity_type="student",
                new_value={"count": len(valid_students)},
                school_id=self.school_id
            )
            
        return {"success": len(valid_students), "errors": errors}

    async def enroll_student(self, data: dict) -> StudentEnrollment:
        # Verify student exists in this school
        student = await self.student_repo.get(data["student_id"])
        if not student:
            raise ValueError("Student not found")

        # Verify section belongs to class
        stmt = select(Section).where(
            Section.school_id == self.school_id,
            Section.id == data["section_id"],
            Section.class_id == data["class_id"],
            Section.academic_year_id == data["academic_year_id"]
        )
        section = (await self.db.execute(stmt)).scalars().first()
        if not section:
            raise ValueError("Invalid section for this class and academic year")

        # Check for active enrollment in the same year
        stmt = select(StudentEnrollment).where(
            StudentEnrollment.school_id == self.school_id,
            StudentEnrollment.student_id == data["student_id"],
            StudentEnrollment.academic_year_id == data["academic_year_id"]
        )
        existing = await self.db.execute(stmt)
        if existing.scalars().first():
            raise ValueError("Student already enrolled for this academic year")

        return await self.enrollment_repo.create(data)

    async def link_guardian(self, student_id: UUID, guardian_id: UUID, data: dict) -> StudentGuardian:
        # Check if already linked
        stmt = select(StudentGuardian).where(
            StudentGuardian.school_id == self.school_id,
            StudentGuardian.student_id == student_id,
            StudentGuardian.guardian_id == guardian_id
        )
        existing = await self.db.execute(stmt)
        if existing.scalars().first():
            raise ValueError("Guardian already linked to this student")

        data["student_id"] = student_id
        data["guardian_id"] = guardian_id
        repo = TenantRepository(StudentGuardian, self.db, self.school_id)
        return await repo.create(data)

    async def assign_teacher(self, data: dict) -> TeacherSubject:
        # Prevent duplicates
        stmt = select(TeacherSubject).where(
            TeacherSubject.school_id == self.school_id,
            TeacherSubject.teacher_id == data["teacher_id"],
            TeacherSubject.section_id == data["section_id"],
            TeacherSubject.subject_id == data["subject_id"],
            TeacherSubject.academic_year_id == data["academic_year_id"]
        )
        existing = await self.db.execute(stmt)
        if existing.scalars().first():
            raise ValueError("Teacher is already assigned to this subject and section")
            
        return await self.assignment_repo.create(data)
