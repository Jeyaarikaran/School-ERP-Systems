# Phase 4: People Management Documentation

## Architecture

Phase 4 separates authentication profiles (Users) from school-specific profiles (Students, Parents, Teachers, Staff).

### Student Architecture
- `Student`: Represents the static identity and profile of a student.
- Contains `admission_number`, `date_of_birth`, demographics.
- Connected to `schools` via `school_id`.

### Enrollment Architecture
- `StudentEnrollment`: Represents the dynamic, time-bound enrollment of a student in a specific section.
- Prevents overriding historical data when a student progresses to the next grade.
- Must match the school context. Overlapping enrollments are blocked by `PeopleService.enroll_student()`.

### Parent-Child Relationship
- `ParentGuardian`: Stores guardian information.
- `StudentGuardian`: Link table that allows M:N relationships (one parent can have multiple students, one student can have multiple guardians).
- APIs enforce IDOR by verifying that a requested student is explicitly linked to the requesting parent.

### Bulk Import
- Designed for scale. Handled via `POST /api/v1/people/students/bulk-import`.
- Processes payload in memory, validating admission numbers in bulk against existing DB records to avoid N+1 querying.
- Saves all valid students in a single transaction.

### Audit Logging
- Operations on people records use the append-only `AuditLog`.
- Logs include `actor_user_id`, `actor_type`, `action`, `entity_id`.
- Automatically strips sensitive keys via `AuditService._redact()`.

## API Spec
- `POST /api/v1/people/students`: Create single student
- `POST /api/v1/people/students/bulk-import`: Create multiple students
- `GET /api/v1/people/students`: List students (paginated)
- `POST /api/v1/people/parents`: Create parent
- `GET /api/v1/people/parents/{id}/children`: List linked children
- `POST /api/v1/people/teachers`: Create teacher
- `POST /api/v1/people/staff`: Create staff
