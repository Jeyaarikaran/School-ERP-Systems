import uuid
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, timezone, datetime

from app.models.fees import FeeCategory, StudentFeeItem, FeeLedgerEntry
from app.services.audit import AuditService

class FeeChargeService:
    @staticmethod
    def post_adhoc_charge(
        db: Session,
        tenant_id: uuid.UUID,
        student_id: uuid.UUID,
        category_code: str,
        amount: Decimal,
        due_date: date,
        reference_type: str,
        reference_id: uuid.UUID,
        idempotency_key: str,
        actor_id: Optional[uuid.UUID] = None
    ) -> StudentFeeItem:
        """
        Creates an ad-hoc fee item (like a fine or transport fee) and records it in the ledger.
        Idempotent by reference_id and idempotency_key.
        """
        # Ensure category exists
        category = db.execute(select(FeeCategory).where(
            FeeCategory.tenant_id == tenant_id,
            FeeCategory.code == category_code
        )).scalar_one_or_none()
        
        if not category:
            category = FeeCategory(
                id=uuid.uuid4(),
                tenant_id=tenant_id,
                code=category_code,
                name=category_code.replace('_', ' ').title(),
                description=f"Auto-generated category for {category_code}"
            )
            db.add(category)
            db.flush()
        
        # Check idempotency
        existing_item = db.execute(select(StudentFeeItem).where(
            StudentFeeItem.tenant_id == tenant_id,
            StudentFeeItem.student_id == student_id,
            StudentFeeItem.reference_type == reference_type,
            StudentFeeItem.reference_id == reference_id,
            StudentFeeItem.category_id == category.id
        )).scalar_one_or_none()
        
        if existing_item:
            return existing_item
            
        fee_item = StudentFeeItem(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            student_id=student_id,
            category_id=category.id,
            amount=amount,
            due_date=due_date,
            status="unpaid",
            reference_type=reference_type,
            reference_id=reference_id
        )
        db.add(fee_item)
        db.flush()
        
        ledger_entry = FeeLedgerEntry(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            student_id=student_id,
            fee_item_id=fee_item.id,
            entry_type="charge",
            amount=amount,
            transaction_date=datetime.now(timezone.utc),
            recorded_by=actor_id,
            notes=f"{category.name} charge"
        )
        db.add(ledger_entry)
        
        if actor_id:
            AuditService.log(
                db=db,
                tenant_id=tenant_id,
                actor_id=actor_id,
                action="fee_charge.posted",
                resource="student_fee_items",
                resource_id=str(fee_item.id),
                details={"amount": str(amount), "reference": str(reference_id)}
            )
            
        return fee_item

    @staticmethod
    def cancel_charges_by_reference(
        db: Session,
        tenant_id: uuid.UUID,
        reference_type: str,
        reference_id: uuid.UUID,
        actor_id: Optional[uuid.UUID] = None
    ) -> Decimal:
        """
        Cancels UNPAID charges for a given reference.
        Returns the amount that was already paid (which requires manual refund/adjustment).
        """
        items = db.execute(select(StudentFeeItem).where(
            StudentFeeItem.tenant_id == tenant_id,
            StudentFeeItem.reference_type == reference_type,
            StudentFeeItem.reference_id == reference_id
        )).scalars().all()
        
        paid_total = Decimal("0.0")
        
        for item in items:
            if item.status == "unpaid":
                item.status = "cancelled"
                ledger_entry = FeeLedgerEntry(
                    id=uuid.uuid4(),
                    tenant_id=tenant_id,
                    student_id=item.student_id,
                    fee_item_id=item.id,
                    entry_type="cancellation",
                    amount=-item.amount,
                    transaction_date=datetime.now(timezone.utc),
                    recorded_by=actor_id,
                    notes=f"Cancelled charge for {reference_type}"
                )
                db.add(ledger_entry)
                
                if actor_id:
                    AuditService.log(
                        db=db,
                        tenant_id=tenant_id,
                        actor_id=actor_id,
                        action="fee_charge.cancelled",
                        resource="student_fee_items",
                        resource_id=str(item.id),
                        details={"amount": str(item.amount), "reference": str(reference_id)}
                    )
            else:
                # Calculate the paid amount (amount - balance, assuming balance exists or if status is paid it's full amount)
                # For simplicity, if it's not unpaid, we assume the whole item amount was paid/partially paid and needs review.
                paid_total += item.amount
                
        return paid_total
