import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, ForeignKey, DateTime, Date, Boolean, Index, UniqueConstraint, Numeric, Integer, text, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from sqlalchemy.orm import relationship

from app.core.database import Base

class LibraryCategory(Base):
    __tablename__ = "library_categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    name_local = Column(String, nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_library_categories_name"),
    )

class LibraryBook(Base):
    __tablename__ = "library_books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    title_local = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    authors = Column(JSONB, nullable=False, default=list) # array of strings
    publisher = Column(String, nullable=True)
    isbn13 = Column(String, nullable=True)
    edition = Column(String, nullable=True)
    publication_year = Column(Integer, nullable=True)
    language = Column(String, nullable=False, default="en")
    category_id = Column(UUID(as_uuid=True), ForeignKey("library_categories.id", ondelete="SET NULL"), nullable=True)
    description = Column(String, nullable=True)
    cover_file_id = Column(UUID(as_uuid=True), nullable=True)
    price = Column(Numeric(12, 2), nullable=True)
    is_reference = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default="active") # active, archived
    search_tsv = Column(TSVECTOR) # populated via trigger
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "isbn13", name="uq_library_books_isbn13"),
        Index("ix_library_books_search", "search_tsv", postgresql_using="gin"),
    )

class LibraryCopy(Base):
    __tablename__ = "library_copies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("library_books.id", ondelete="CASCADE"), nullable=False)
    accession_no = Column(String, nullable=False)
    barcode = Column(String, nullable=False)
    shelf_location = Column(String, nullable=True)
    condition = Column(String, nullable=False, default="good") # new, good, fair, poor
    status = Column(String, nullable=False, default="available") # available, issued, lost, damaged, in_repair, missing, withdrawn
    acquired_on = Column(Date, nullable=True)
    price = Column(Numeric(12, 2), nullable=True)
    supplier = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "accession_no", name="uq_library_copies_accession"),
        UniqueConstraint("tenant_id", "barcode", name="uq_library_copies_barcode"),
        Index("ix_library_copies_book", "book_id", "status"),
    )

class LibraryMember(Base):
    __tablename__ = "library_members"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    member_type = Column(String, nullable=False) # student, staff
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=True)
    member_no = Column(String, nullable=False)
    barcode = Column(String, nullable=False)
    status = Column(String, nullable=False, default="active") # active, suspended, expired
    suspended_reason = Column(String, nullable=True)
    joined_on = Column(Date, nullable=False, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "member_no", name="uq_library_members_no"),
        UniqueConstraint("tenant_id", "barcode", name="uq_library_members_barcode"),
        UniqueConstraint("tenant_id", "student_id", name="uq_library_members_student"),
        UniqueConstraint("tenant_id", "staff_id", name="uq_library_members_staff"),
    )

class BookIssue(Base):
    __tablename__ = "book_issues"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    copy_id = Column(UUID(as_uuid=True), ForeignKey("library_copies.id", ondelete="RESTRICT"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("library_members.id", ondelete="RESTRICT"), nullable=False)
    issued_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_date = Column(Date, nullable=False)
    returned_at = Column(DateTime(timezone=True), nullable=True)
    issued_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    returned_to = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    renewal_count = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default="issued") # issued, returned, lost
    notes = Column(String, nullable=True)
    
    __table_args__ = (
        Index("ix_book_issues_active_copy", "copy_id", postgresql_where=text("returned_at IS NULL AND status = 'issued'"), unique=True),
        Index("ix_book_issues_member", "member_id", "status"),
    )

class LibraryCirculationEvent(Base):
    __tablename__ = "library_circulation_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("book_issues.id", ondelete="CASCADE"), nullable=True)
    copy_id = Column(UUID(as_uuid=True), ForeignKey("library_copies.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("library_members.id", ondelete="CASCADE"), nullable=True)
    event_type = Column(String, nullable=False) # issue, return, renew, mark_lost, mark_damaged, override, status_change, withdraw_copy
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    request_id = Column(String, nullable=True) # idempotency tracking
    metadata_ = Column("metadata", JSONB, nullable=True) # details like override reason

class LibraryFine(Base):
    __tablename__ = "library_fines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("library_members.id", ondelete="CASCADE"), nullable=False)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("book_issues.id", ondelete="CASCADE"), nullable=True)
    kind = Column(String, nullable=False) # overdue, lost, damaged, manual
    amount = Column(Numeric(12, 2), nullable=False)
    days_overdue = Column(Integer, nullable=True)
    assessed_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String, nullable=False, default="pending") # pending, paid, waived, cancelled
    waived_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    waive_reason = Column(String, nullable=True)
    fee_item_id = Column(UUID(as_uuid=True), nullable=True) # Cross-module ID tracking
    settled_via = Column(String, nullable=True) # fee_ledger, librarian_cash
    settled_reference = Column(String, nullable=True)

class LibraryStocktake(Base):
    __tablename__ = "library_stocktakes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    scope_type = Column(String, nullable=False) # all, shelf, category
    scope_value = Column(String, nullable=True)
    status = Column(String, nullable=False, default="open") # open, closed
    started_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    closed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    closed_at = Column(DateTime(timezone=True), nullable=True)

class LibraryStocktakeScan(Base):
    __tablename__ = "library_stocktake_scans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stocktake_id = Column(UUID(as_uuid=True), ForeignKey("library_stocktakes.id", ondelete="CASCADE"), nullable=False)
    copy_id = Column(UUID(as_uuid=True), ForeignKey("library_copies.id", ondelete="CASCADE"), nullable=False)
    scanned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    scanned_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    found_location = Column(String, nullable=True)
    
    __table_args__ = (
        UniqueConstraint("stocktake_id", "copy_id", name="uq_library_stocktake_scans_copy"),
    )
