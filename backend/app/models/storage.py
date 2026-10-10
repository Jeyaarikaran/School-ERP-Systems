"""Storage and Bulk Import/Export models."""

from uuid import UUID
from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
import enum

from app.core.database import Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin


class FileStatus(str, enum.Enum):
    PENDING_SCAN = "pending_scan"
    CLEAN = "clean"
    INFECTED = "infected"
    REJECTED = "rejected"


class FileMetadata(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Metadata for all objects stored in S3/MinIO."""
    __tablename__ = "file_metadata"

    storage_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    
    owner_entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., 'student'
    owner_entity_id: Mapped[str] = mapped_column(String(50), nullable=False)
    
    status: Mapped[FileStatus] = mapped_column(SQLEnum(FileStatus), default=FileStatus.PENDING_SCAN, nullable=False)
    checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)  # SHA-256


class Document(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Specific documents attached to students (birth certificate, TC, etc.)."""
    __tablename__ = "documents"

    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file_metadata.id", ondelete="CASCADE"), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)


class JobStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    VALIDATING = "validating"
    VALIDATED = "validated"
    FAILED = "failed"
    COMMITTING = "committing"
    COMPLETED = "completed"


class ImportJob(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """State tracking for bulk import operations."""
    __tablename__ = "import_jobs"

    job_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'students', 'staff'
    status: Mapped[JobStatus] = mapped_column(SQLEnum(JobStatus), default=JobStatus.UPLOADED, nullable=False)
    
    source_file_id: Mapped[UUID] = mapped_column(ForeignKey("file_metadata.id", ondelete="CASCADE"), nullable=False)
    report_file_id: Mapped[UUID | None] = mapped_column(ForeignKey("file_metadata.id", ondelete="SET NULL"), nullable=True)
    
    total_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    valid_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    created_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
