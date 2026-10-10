"""S3-compatible Storage Service and Malware scanning."""

import os
import uuid
from typing import Protocol, BinaryIO

class MalwareScanner(Protocol):
    def scan(self, file: BinaryIO) -> bool:
        """Returns True if clean, False if infected."""
        ...

class NoOpScanner:
    """Development scanner that always passes."""
    def scan(self, file: BinaryIO) -> bool:
        if os.getenv("ENVIRONMENT") != "development":
            import logging
            logging.warning("NoOpScanner is running outside development!")
        return True


class StorageService:
    """Wraps MinIO/S3 for presigned URLs and uploads."""
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, bucket_name: str, scanner: MalwareScanner):
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.scanner = scanner

    def generate_presigned_url(self, storage_key: str, expires_in: int = 300) -> str:
        """Generate a short-lived download URL."""
        # Stub: Implement boto3 or minio SDK client logic here.
        return f"{self.endpoint_url}/{self.bucket_name}/{storage_key}?signature=signed"

    def upload_file(self, school_id: uuid.UUID, category: str, original_filename: str, file: BinaryIO, content_type: str) -> str:
        """Validates and uploads file to object storage, returning the storage key."""
        if not self.scanner.scan(file):
            raise ValueError("Malware detected in upload.")
        
        # Reset file pointer after scan
        file.seek(0)
        
        # Generate clean storage key: {school_id}/{category}/{yyyy}/{uuid}
        from datetime import datetime
        year = datetime.utcnow().year
        file_uuid = str(uuid.uuid4())
        key = f"{school_id}/{category}/{year}/{file_uuid}"
        
        # Stub: Implement actual s3 put_object logic here.
        
        return key
