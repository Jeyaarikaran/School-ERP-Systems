# Phase 4 Report: Attendance and Offline Sync

## 1. What was built
- **Core Attendance Models:** `AttendanceSession`, `AttendanceRecord`, `AttendanceHistory`, `AttendanceCorrection`, and `SchoolCalendarDay` implemented via SQLAlchemy schemas.
- **Offline Sync & Outbox Models:** `AttendanceSyncOp` implemented as the op-level idempotency store for offline batch sync, and `OutboxEvent` built for transactional messaging.
- **Performance Optimizations:** `AttendanceDailySummary` created for denormalized counting to ensure fast dashboard rendering. Denormalized `attendance_date` on records added for range partitioning readiness.
- **Conflict Resolution Engine:** Implemented pure function `resolve_offline_batch()` in `AttendanceEngine` to handle the complex state matrix of offline submissions merging with server state via optimistic record-level versioning.
- **Statistical Calculators:** Designed pure statistical calculator for dynamically determining compliance and percentages, skipping excused/leaves from the denominator.
- **RBAC Integrations:** Replaced placeholder attendance permissions with detailed catalog entries (`attendance.view`, `.create`, `.update`, `.approve`, `.export`, `.settings`, `calendar.manage`). 

## 2. Acceptance Checklist
- [x] Migrations defined via SQLAlchemy models (Pending Alembic autogenerate).
- [x] Record-level optimistic locking handled.
- [x] Idempotency store isolates offline sync operations.
- [x] Pure domain logic isolates complex calculations from DB connections.
- [⚠️] Test Suite Verification: Blocked. Cannot execute `uv run pytest` due to environment constraints.

## 3. Measured Performance Numbers
**Pending local execution.** Execution blocked by environment constraints (no PowerShell). 
- *Target:* Sync batch of 10 ops × 60 students should resolve in p95 < 1.5s utilizing `INSERT ... ON CONFLICT` batching. 

## 4. ADRs Added & Deviations
- **ADR-018: Daily-only Attendance.** Scoped attendance strictly to daily mode for now to ensure extreme reliability, though schema leaves room for period-wise later via `session_type`.
- **ADR-019: Record-level Versioning.** Opted for resolving offline conflicts at the student record level rather than the session level. A single student conflict should never reject the entire class sync operation.
- **ADR-020: Op-level Idempotency Store.** Introduced `attendance_sync_ops` directly to handle client `client_op_id` retries independently of the generic API layer, making it extremely resilient to network drops.
- **ADR-021: Outbox Pattern.** Chose to transactionally append `outbox_events` alongside attendance changes instead of dispatching direct Celery events. This guarantees no dropped webhook triggers on transaction rollback.

## 5. Known Limitations and Risks
- **Terminal Execution Constraint:** The automated agent was unable to execute any terminal commands (`make migrate`, `pytest`, `k6`) due to a missing PowerShell binary path. Testing and Alembic migration generation must be performed locally.
- **Frontend Sync Engine:** The complex Mobile Drift queue state machine is documented logically but has not been scaffolded into Dart code yet due to interactive shell blockages. 

## 6. Proposed First Steps for Phase 5
1. Run `make setup` and `alembic revision --autogenerate -m "attendance_and_offline_sync"` locally.
2. Build the Timetable module schemas (rooms, periods, class periods).
3. Connect the `OutboxEvent` publisher to a Celery Beat task.
