"""Report Engine — Async report execution and format generation."""

import csv
import io
from uuid import UUID
from datetime import datetime, timezone
from typing import Protocol, Any, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reports import ReportJob, ReportJobStatus

class ReportWriter(Protocol):
    def write(self, data: List[Dict[str, Any]]) -> bytes:
        ...

class CSVWriter:
    def write(self, data: List[Dict[str, Any]]) -> bytes:
        if not data:
            return b""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue().encode("utf-8")


class ReportEngine:
    @staticmethod
    async def create_job(
        db: AsyncSession,
        tenant_id: UUID,
        requester_id: UUID,
        definition_key: str,
        params: dict,
        format_type: str,
        is_sensitive: bool = False,
        reason: str | None = None
    ) -> ReportJob:
        # 7 days expiry by default
        from datetime import timedelta
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        job = ReportJob(
            school_id=tenant_id,
            requester_id=requester_id,
            definition_key=definition_key,
            params=params,
            format=format_type,
            status=ReportJobStatus.QUEUED,
            is_sensitive=is_sensitive,
            reason=reason,
            queued_at=datetime.now(timezone.utc),
            expires_at=expires_at
        )
        db.add(job)
        # In a real app, enqueue celery task here
        return job

