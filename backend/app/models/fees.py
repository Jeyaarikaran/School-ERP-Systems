"""Fees, Payments, Receipts, and Financial Ledger Models."""

from datetime import date, datetime
from uuid import UUID
import enum

from sqlalchemy import String, Integer, ForeignKey, Date, DateTime, Boolean, Numeric, Enum as SQLEnum, UniqueConstraint, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


# ---------------------------------------------------------
# Fee Catalog
# ---------------------------------------------------------
class FeeCategory(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "fee_categories"
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    name_local: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_refundable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    accounting_code: Mapped[str | None] = mapped_column(String(50), nullable=True)

class FeeStructureStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"

class FeeStructure(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "fee_structures"
    academic_year_id: Mapped[UUID] = mapped_column(ForeignKey("academic_years.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[FeeStructureStatus] = mapped_column(SQLEnum(FeeStructureStatus), default=FeeStructureStatus.DRAFT, nullable=False)

class FeeStructureClass(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "fee_structure_classes"
    structure_id: Mapped[UUID] = mapped_column(ForeignKey("fee_structures.id", ondelete="CASCADE"), nullable=False)
    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    __table_args__ = (UniqueConstraint("structure_id", "class_id", name="uq_fee_structure_class"),)

class ScheduleType(str, enum.Enum):
    ONE_TIME = "one_time"
    INSTALLMENTS = "installments"

class FeeStructureItem(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "fee_structure_items"
    structure_id: Mapped[UUID] = mapped_column(ForeignKey("fee_structures.id", ondelete="CASCADE"), index=True, nullable=False)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("fee_categories.id", ondelete="RESTRICT"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    schedule_type: Mapped[ScheduleType] = mapped_column(SQLEnum(ScheduleType), default=ScheduleType.ONE_TIME, nullable=False)

class FeeInstallment(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "fee_installments"
    structure_item_id: Mapped[UUID] = mapped_column(ForeignKey("fee_structure_items.id", ondelete="CASCADE"), index=True, nullable=False)
    installment_no: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

class LateFeeRuleCalc(str, enum.Enum):
    FLAT_ONCE = "flat_once"
    PER_DAY = "per_day"
    PER_MONTH = "per_month"

class LateFeeRule(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "late_fee_rules"
    # Null structure_id means school default
    structure_id: Mapped[UUID | None] = mapped_column(ForeignKey("fee_structures.id", ondelete="CASCADE"), nullable=True)
    grace_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    calculation: Mapped[LateFeeRuleCalc] = mapped_column(SQLEnum(LateFeeRuleCalc), nullable=False)
    rate: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False) # Fixed amount or percent
    cap_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    applies_to_category_ids: Mapped[list[str]] = mapped_column(JSONB, nullable=False) # List of UUIDs


# ---------------------------------------------------------
# Adjustments (Discounts, Scholarships)
# ---------------------------------------------------------
class AdjustmentKind(str, enum.Enum):
    DISCOUNT = "discount"
    SCHOLARSHIP = "scholarship"
    CONCESSION = "concession"
    SIBLING = "sibling"

class AdjustmentCalc(str, enum.Enum):
    PERCENT = "percent"
    FIXED = "fixed"

class AdjustmentTemplate(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "adjustment_templates"
    kind: Mapped[AdjustmentKind] = mapped_column(SQLEnum(AdjustmentKind), nullable=False)
    calculation: Mapped[AdjustmentCalc] = mapped_column(SQLEnum(AdjustmentCalc), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    applies_to_category_ids: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    valid_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    valid_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    approval_threshold: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)

class AdjustmentStatus(str, enum.Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVOKED = "revoked"

class StudentAdjustment(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "student_adjustments"
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    template_id: Mapped[UUID | None] = mapped_column(ForeignKey("adjustment_templates.id", ondelete="SET NULL"), nullable=True)
    calculation: Mapped[AdjustmentCalc] = mapped_column(SQLEnum(AdjustmentCalc), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[AdjustmentStatus] = mapped_column(SQLEnum(AdjustmentStatus), default=AdjustmentStatus.REQUESTED, nullable=False)
    
    requested_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    approved_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ---------------------------------------------------------
# Student Fees
# ---------------------------------------------------------
class StudentFeeItemStatus(str, enum.Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    WAIVED = "waived"
    CANCELLED = "cancelled"

class StudentFeeItem(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "student_fee_items"
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    enrollment_id: Mapped[UUID] = mapped_column(ForeignKey("student_enrollments.id", ondelete="CASCADE"), nullable=False)
    structure_item_id: Mapped[UUID] = mapped_column(ForeignKey("fee_structure_items.id", ondelete="RESTRICT"), nullable=False)
    installment_id: Mapped[UUID | None] = mapped_column(ForeignKey("fee_installments.id", ondelete="RESTRICT"), nullable=True)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("fee_categories.id", ondelete="RESTRICT"), nullable=False)
    
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    gross_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    late_fee_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    
    # In PostgreSQL, this would ideally be: GENERATED ALWAYS AS (gross_amount - discount_amount + late_fee_amount) STORED
    # Using python-side default for abstract models before migration implementation
    net_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False) 
    
    paid_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    refunded_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    status: Mapped[StudentFeeItemStatus] = mapped_column(SQLEnum(StudentFeeItemStatus), default=StudentFeeItemStatus.PENDING, nullable=False)
    
    __table_args__ = (
        UniqueConstraint("student_id", "structure_item_id", "installment_id", name="uq_student_fee_item"),
        CheckConstraint("gross_amount >= 0", name="chk_gross_amount_pos"),
        CheckConstraint("paid_amount >= 0", name="chk_paid_amount_pos"),
        CheckConstraint("paid_amount <= net_amount", name="chk_paid_amount_max"),
        CheckConstraint("refunded_amount <= paid_amount", name="chk_refunded_amount_max")
    )


# ---------------------------------------------------------
# Fee Ledger
# ---------------------------------------------------------
class LedgerEntryType(str, enum.Enum):
    CHARGE = "charge"
    DISCOUNT = "discount"
    LATE_FEE = "late_fee"
    PAYMENT = "payment"
    REFUND = "refund"
    REVERSAL = "reversal"
    WRITEOFF = "writeoff"
    CREDIT_IN = "credit_in"
    CREDIT_OUT = "credit_out"

class FeeLedgerEntry(Base, UUIDPrimaryKeyMixin, TenantMixin):
    __tablename__ = "fee_ledger_entries"
    # Immutable append-only table. No updated_at.
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    student_fee_item_id: Mapped[UUID | None] = mapped_column(ForeignKey("student_fee_items.id", ondelete="CASCADE"), nullable=True)
    
    entry_type: Mapped[LedgerEntryType] = mapped_column(SQLEnum(LedgerEntryType), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False) # Signed
    
    reference_type: Mapped[str] = mapped_column(String(50), nullable=False) # e.g. "payment", "adjustment"
    reference_id: Mapped[UUID | None] = mapped_column(ForeignKey("fee_payments.id", ondelete="SET NULL"), nullable=True)
    
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


# ---------------------------------------------------------
# Payments & Allocations
# ---------------------------------------------------------
class PaymentMode(str, enum.Enum):
    CASH = "cash"
    CHEQUE = "cheque"
    BANK_TRANSFER = "bank_transfer"
    UPI_OFFLINE = "upi_offline"
    CARD_POS = "card_pos"
    ONLINE = "online"

class PaymentStatus(str, enum.Enum):
    INITIATED = "initiated"
    PENDING = "pending"
    CAPTURED = "captured"
    FAILED = "failed"
    CANCELLED = "cancelled"
    VOIDED = "voided"
    BOUNCED = "bounced"

class FeePayment(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "fee_payments"
    payer_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    payer_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    
    mode: Mapped[PaymentMode] = mapped_column(SQLEnum(PaymentMode), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), nullable=False)
    
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    
    gateway_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gateway_order_id: Mapped[str | None] = mapped_column(String(150), nullable=True)
    gateway_payment_id: Mapped[str | None] = mapped_column(String(150), nullable=True)
    reference_no: Mapped[str | None] = mapped_column(String(100), nullable=True) # Cheque/UTR
    
    received_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    collected_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    
    idempotency_key: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_code: Mapped[str | None] = mapped_column(String(100), nullable=True)


class PaymentAllocation(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "payment_allocations"
    payment_id: Mapped[UUID] = mapped_column(ForeignKey("fee_payments.id", ondelete="CASCADE"), index=True, nullable=False)
    student_fee_item_id: Mapped[UUID] = mapped_column(ForeignKey("student_fee_items.id", ondelete="RESTRICT"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)


# ---------------------------------------------------------
# Receipts & Refunds
# ---------------------------------------------------------
class ReceiptStatus(str, enum.Enum):
    VALID = "valid"
    CANCELLED = "cancelled"

class FeeReceipt(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "fee_receipts"
    # Immutable payload.
    receipt_no: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    payment_id: Mapped[UUID] = mapped_column(ForeignKey("fee_payments.id", ondelete="RESTRICT"), nullable=False)
    
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    issued_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    
    snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[ReceiptStatus] = mapped_column(SQLEnum(ReceiptStatus), default=ReceiptStatus.VALID, nullable=False)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    cancel_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    verification_token: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    pdf_file_id: Mapped[UUID | None] = mapped_column(ForeignKey("file_metadata.id", ondelete="SET NULL"), nullable=True)


class ReceiptCounter(Base, TenantMixin):
    __tablename__ = "receipt_counters"
    # Composite primary key (tenant_id, prefix, fy)
    prefix: Mapped[str] = mapped_column(String(20), primary_key=True)
    financial_year: Mapped[str] = mapped_column(String(10), primary_key=True)
    last_seq: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class RefundStatus(str, enum.Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class RefundMode(str, enum.Enum):
    GATEWAY = "gateway"
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CREDIT = "credit"

class FeeRefund(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "fee_refunds"
    payment_id: Mapped[UUID] = mapped_column(ForeignKey("fee_payments.id", ondelete="RESTRICT"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    mode: Mapped[RefundMode] = mapped_column(SQLEnum(RefundMode), nullable=False)
    status: Mapped[RefundStatus] = mapped_column(SQLEnum(RefundStatus), default=RefundStatus.REQUESTED, nullable=False)
    
    requested_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    approved_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    gateway_refund_id: Mapped[str | None] = mapped_column(String(150), nullable=True)
    credit_note_no: Mapped[str | None] = mapped_column(String(50), nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(100), nullable=True)


# ---------------------------------------------------------
# Webhooks and Closing
# ---------------------------------------------------------
class WebhookEventStatus(str, enum.Enum):
    RECEIVED = "received"
    PROCESSED = "processed"
    FAILED = "failed"
    UNMATCHED = "unmatched"

class WebhookEvent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "webhook_events"
    # Not purely tenant scoped initially, tenant resolved from account payload
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    event_id: Mapped[str] = mapped_column(String(150), nullable=False)
    school_id: Mapped[UUID | None] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"), nullable=True)
    
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[WebhookEventStatus] = mapped_column(SQLEnum(WebhookEventStatus), default=WebhookEventStatus.RECEIVED, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    
    __table_args__ = (UniqueConstraint("provider", "event_id", name="uq_webhook_event"),)


class FeeDayClosure(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    __tablename__ = "fee_day_closures"
    business_date: Mapped[date] = mapped_column(Date, nullable=False)
    closed_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    closed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    totals_by_mode: Mapped[dict] = mapped_column(JSONB, nullable=False)
    totals_by_collector: Mapped[dict] = mapped_column(JSONB, nullable=False)
    
    __table_args__ = (UniqueConstraint("school_id", "business_date", name="uq_day_closure"),)
