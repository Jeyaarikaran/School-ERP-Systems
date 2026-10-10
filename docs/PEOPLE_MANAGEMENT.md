# People Management (Phase 4)

## Overview
Phase 4 separates authentication profiles (Users) from school-specific profiles (Students, Parents, Teachers, Staff).

## Student Architecture
- `Student`: Represents the static identity and profile of a student.
- `StudentEnrollment`: Represents the dynamic, time-bound enrollment of a student in a specific section. Must match the school context. Overlapping enrollments are blocked by `PeopleService.enroll_student()`.

## Parent-Child Relationship
- `ParentGuardian`: Stores guardian information.
- `StudentGuardian`: Link table that allows M:N relationships. APIs enforce IDOR by verifying that a requested student is explicitly linked to the requesting parent.

## Bulk Import
- Designed for scale. Handled via `POST /api/v1/people/students/bulk-import`.
- Processes payload in memory, validating admission numbers in bulk against existing DB records to avoid N+1 querying.

## Audit Logging
- Operations on people records use the append-only `AuditLog`.
- Automatically strips sensitive keys via `AuditService._redact()`.
