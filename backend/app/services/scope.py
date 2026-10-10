"""Scope resolvers for row-level visibility and filtering."""

from uuid import UUID
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.sql.elements import BinaryExpression

from app.models.people import TeacherSubject, StudentGuardian, StudentEnrollment


class ScopeResolver(Protocol):
    """Protocol for resolving the subset of data a user is allowed to see."""
    def get_student_filter(self, student_model: type) -> BinaryExpression | None:
        """Return a SQLAlchemy filter expression for students, or None if no access."""
        ...
        
    def get_section_filter(self, section_model: type) -> BinaryExpression | None:
        """Return a SQLAlchemy filter expression for sections, or None if no access."""
        ...


class AdminScopeResolver:
    """Super Admin, School Admin, Principal see everything in their school."""
    def get_student_filter(self, student_model: type) -> BinaryExpression | None:
        return True  # Type-wise it works, handled by TenantRepository

    def get_section_filter(self, section_model: type) -> BinaryExpression | None:
        return True


class TeacherScopeResolver:
    """Teachers see sections they are assigned to, and enrolled students therein."""
    def __init__(self, staff_id: UUID, academic_year_id: UUID):
        self.staff_id = staff_id
        self.academic_year_id = academic_year_id

    def _assigned_sections_stmt(self):
        return (
            select(TeacherSubject.section_id)
            .where(
                TeacherSubject.teacher_id == self.staff_id,
                TeacherSubject.academic_year_id == self.academic_year_id
            )
        )

    def get_student_filter(self, student_model: type) -> BinaryExpression | None:
        # A subquery checking if the student has an enrollment in an assigned section
        return student_model.id.in_(
            select(StudentEnrollment.student_id)
            .where(
                StudentEnrollment.academic_year_id == self.academic_year_id,
                StudentEnrollment.section_id.in_(self._assigned_sections_stmt())
            )
        )

    def get_section_filter(self, section_model: type) -> BinaryExpression | None:
        return section_model.id.in_(self._assigned_sections_stmt())


class ParentScopeResolver:
    """Parents see only children linked to them."""
    def __init__(self, user_id: UUID):
        self.user_id = user_id

    def get_student_filter(self, student_model: type) -> BinaryExpression | None:
        return student_model.id.in_(
            select(StudentGuardian.student_id)
            .join(StudentGuardian.guardian)
            .where(StudentGuardian.guardian.has(user_id=self.user_id))
        )

    def get_section_filter(self, section_model: type) -> BinaryExpression | None:
        # A parent might need to see the section their child is in, but usually they
        # just view the child's profile. We limit section visibility strictly.
        return section_model.id.in_(
            select(StudentEnrollment.section_id)
            .where(StudentEnrollment.student_id.in_(
                select(StudentGuardian.student_id)
                .join(StudentGuardian.guardian)
                .where(StudentGuardian.guardian.has(user_id=self.user_id))
            ))
        )


class StudentScopeResolver:
    """Students see only themselves."""
    def __init__(self, user_id: UUID):
        self.user_id = user_id

    def get_student_filter(self, student_model: type) -> BinaryExpression | None:
        return student_model.user_id == self.user_id

    def get_section_filter(self, section_model: type) -> BinaryExpression | None:
        return section_model.id.in_(
            select(StudentEnrollment.section_id)
            .join(StudentEnrollment.student)
            .where(StudentEnrollment.student.has(user_id=self.user_id))
        )
