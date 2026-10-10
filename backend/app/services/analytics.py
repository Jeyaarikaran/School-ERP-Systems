"""Rollup Service — Incremental aggregations."""

from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.analytics import RollupRun

class RollupService:
    @staticmethod
    async def track_run(
        db: AsyncSession,
        tenant_id: UUID,
        rollup_key: str,
        window_start: date,
        window_end: date
    ) -> RollupRun:
        """Records that a rollup run started."""
        from datetime import datetime, timezone
        
        run = RollupRun(
            school_id=tenant_id,
            rollup_key=rollup_key,
            window_start=window_start,
            window_end=window_end,
            status="running",
            started_at=datetime.now(timezone.utc)
        )
        db.add(run)
        return run
        
    @staticmethod
    async def complete_run(
        db: AsyncSession,
        run_id: UUID,
        rows_upserted: int
    ) -> None:
        """Records successful completion."""
        from datetime import datetime, timezone
        run = await db.get(RollupRun, run_id)
        if run:
            run.status = "completed"
            run.rows_upserted = rows_upserted
            run.finished_at = datetime.now(timezone.utc)
            run.duration_ms = int((run.finished_at - run.started_at).total_seconds() * 1000)
