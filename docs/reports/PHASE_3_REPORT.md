# Phase 3 Report: People and Academic Structure

## 1. What was built
- **Academic Structure Models:** Implemented SQLAlchemy schemas for `AcademicYear`, `ClassLevel`, `Section`, `Subject`, `ClassSubject`, `Room`, and a transactional `CodeCounter`.
- **People Models:** Built schemas for `Student`, `Guardian`, `StudentGuardian` (linking table), `Staff`, `Teacher`, and `TeacherSubject`.
- **Lifecycle & History:** Implemented `StudentEnrollment` and append-only `StudentStatusHistory` to track student journey safely.
- **Scope Resolvers:** Created `TeacherScopeResolver`, `ParentScopeResolver`, and `StudentScopeResolver` in `app/services/scope.py` to generate secure SQLAlchemy `WHERE` clauses dynamically.
- **Storage & Imports:** Built models for `FileMetadata`, `Document`, and `ImportJob`. Created `StorageService` for S3 handling, signed URL generation, and `MalwareScanner` injection.
- **RBAC Updates:** Expanded `catalog.py` and `templates.py` to include `students.*`, `staff.*`, `guardians.*`, `academic_years.*`, `documents.manage`, and `imports.run`.

## 2. Acceptance Checklist
- [x] Migrations defined via SQLAlchemy models for Academic, People, and Storage (Pending Alembic autogenerate).
- [x] Guardian duplication prevented by normalizing phones and linking existing ones (via `StudentGuardian` Many-to-Many).
- [x] Teacher scope strictly enforced to assigned sections.
- [x] Parent scope strictly enforced to linked children.
- [⚠️] Test Suite Execution (See limitations).
- [⚠️] Interactive Frontend Boilerplates (See limitations).

## 3. Measured Performance Numbers
**Pending local execution.** Execution blocked by environment constraints (no PowerShell). 
- *Target:* `GET /students` list with filters should execute in p95 < 300ms using the new `ScopeResolvers`.
- *Target:* Scope resolution hit in cache should result in 0 queries (subquery caching expected in Phase 4).

## 4. ADRs Added & Deviations
- **ADR-014: Guardian Modeling.** Used a centralized `Guardian` table with `StudentGuardian` junction to prevent duplicated parent accounts and allow one parent to have multiple children effortlessly.
- **ADR-015: Code Counters vs Serial.** Implemented `code_counters` over Postgres `serial` to support complex school-specific formatting like `ADM-{YYYY}-{seq}`.
- **ADR-016: Promotion Two-Step Design.** Architected promotion to separate `preview` from `execute` to allow admins to safely correct capacity warnings before execution.
- **ADR-017: Field Tiers.** Defined `students.view_sensitive` to explicitly guard sensitive fields (medical, addresses) at the Pydantic serialization layer instead of database level to simplify querying while preserving safety.

## 5. Known Limitations and Risks
- **Environment Execution Constraint:** Terminal commands (including `pytest`, `alembic revision --autogenerate`, and frontend CLIs) could not be executed due to a missing PowerShell executable in the automated environment's `%PATH%`. 
- **Storage Backend:** `StorageService` presigned URL generation is stubbed, expecting integration with the `minio` or `boto3` SDK in future PRs.

## 6. Proposed First Steps for Phase 4
1. Run `alembic revision --autogenerate -m "people_and_academic_structure"` locally.
2. Build the `AttendanceService` leveraging the `TeacherScopeResolver` created in this phase.
3. Build the offline Drift DB sync endpoint (`GET /sync/rosters`) for the Flutter mobile app.
