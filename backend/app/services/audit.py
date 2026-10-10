"""Audit service for append-only transactional logging."""

import json
from uuid import UUID
from typing import Any
from fastapi import Request

from app.core.database import AsyncSession
from app.models.audit import AuditLog


class AuditService:
    """Service to record audit logs transactionally."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def record(
        self,
        actor_user_id: UUID | None,
        actor_type: str,
        action: str,
        entity_type: str,
        entity_id: str | None = None,
        old_value: dict[str, Any] | None = None,
        new_value: dict[str, Any] | None = None,
        school_id: UUID | None = None,
        request: Request | None = None,
    ) -> None:
        """Record an audit event. MUST be called within the same transaction as the change."""
        # Sanitize sensitive fields before persisting
        safe_old = self._redact(old_value) if old_value else None
        safe_new = self._redact(new_value) if new_value else None

        ip_address = None
        user_agent = None
        request_id = None
        if request:
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent", "")[:200]
            request_id = getattr(request.state, "request_id", None)

        log_entry = AuditLog(
            school_id=school_id,
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=safe_old,
            new_value=safe_new,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
        )
        self.db_session.add(log_entry)
        # Flush to ensure it's written in this transaction
        await self.db_session.flush()

    def _redact(self, data: dict[str, Any]) -> dict[str, Any]:
        """Redact sensitive fields from audit payload."""
        SENSITIVE = {"password", "password_hash", "token", "secret", "code", "otp"}
        clean = {}
        for k, v in data.items():
            if any(s in k.lower() for s in SENSITIVE):
                clean[k] = "***REDACTED***"
            elif isinstance(v, dict):
                clean[k] = self._redact(v)
            else:
                clean[k] = v
        return clean
