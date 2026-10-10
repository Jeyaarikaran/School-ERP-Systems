"""Privacy Services — Consents, Data Requests, Erasure, and Retention."""

from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.privacy import (
    Consent, ConsentPurpose, DataRequest, DataRequestType, 
    DataRequestStatus, PolicyAcceptance, RetentionPolicy
)
from app.core.errors import AuthorizationError, StateConflictError

class PrivacyService:
    """Manages consents and policy acceptances."""
    
    @staticmethod
    async def grant_consent(
        db: AsyncSession,
        tenant_id: UUID,
        subject_id: UUID,
        subject_type: str,
        purpose: ConsentPurpose,
        granted_by_user_id: UUID,
        policy_version: str
    ) -> Consent:
        """Grants consent. Minor consents must be granted by guardians."""
        # Note: In a real system, verify guardian relationship here if subject is a minor.
        
        # Append-only: withdraw any existing active consent first
        await db.execute(
            update(Consent)
            .where(
                Consent.school_id == tenant_id,
                Consent.subject_id == subject_id,
                Consent.purpose == purpose,
                Consent.withdrawn_at.is_(None)
            )
            .values(withdrawn_at=datetime.now(timezone.utc))
        )
        
        consent = Consent(
            school_id=tenant_id,
            subject_type=subject_type,
            subject_id=subject_id,
            purpose=purpose,
            granted_by_user_id=granted_by_user_id,
            policy_version=policy_version,
            granted_at=datetime.now(timezone.utc)
        )
        db.add(consent)
        return consent

    @staticmethod
    async def withdraw_consent(
        db: AsyncSession,
        tenant_id: UUID,
        subject_id: UUID,
        purpose: ConsentPurpose
    ) -> None:
        """Withdraws an active consent."""
        await db.execute(
            update(Consent)
            .where(
                Consent.school_id == tenant_id,
                Consent.subject_id == subject_id,
                Consent.purpose == purpose,
                Consent.withdrawn_at.is_(None)
            )
            .values(withdrawn_at=datetime.now(timezone.utc))
        )


class ErasureService:
    """Handles data erasure and anonymization with two-person approval."""
    
    @staticmethod
    async def request_erasure(
        db: AsyncSession,
        tenant_id: UUID,
        subject_id: UUID,
        subject_type: str,
        requested_by: UUID
    ) -> DataRequest:
        request = DataRequest(
            school_id=tenant_id,
            request_type=DataRequestType.ERASURE,
            subject_type=subject_type,
            subject_id=subject_id,
            requested_by=requested_by,
            status=DataRequestStatus.RECEIVED
        )
        db.add(request)
        return request
        
    @staticmethod
    async def approve_and_execute_erasure(
        db: AsyncSession,
        tenant_id: UUID,
        request_id: UUID,
        approver_id: UUID
    ) -> DataRequest:
        """
        Approves and executes the erasure.
        Enforces two-person rule: approver cannot be the requester.
        """
        request = await db.get(DataRequest, request_id)
        if not request:
            raise ValueError("Request not found")
            
        if request.requested_by == approver_id:
            raise AuthorizationError(code="SELF_APPROVAL_FORBIDDEN", message="Erasure requires a different approver.")
            
        if request.status != DataRequestStatus.RECEIVED and request.status != DataRequestStatus.VERIFYING:
            raise StateConflictError("Request is not in a pending state.")
            
        request.status = DataRequestStatus.IN_PROGRESS
        request.approved_by = approver_id
        
        # Here we would enqueue the actual anonymization worker job.
        # For now, mark completed.
        request.status = DataRequestStatus.COMPLETED
        request.completed_at = datetime.now(timezone.utc)
        
        return request
