"""Application configuration — pydantic-settings, fail-fast validation."""

from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Fails fast on startup if required values are missing or invalid.
    """

    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- Application ----
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = True
    app_secret_key: str = "change-me-in-production"
    app_allowed_hosts: list[str] = ["localhost", "127.0.0.1"]

    # ---- Database ----
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "school_erp"
    db_user: str = "school_erp"
    db_password: SecretStr = SecretStr("change-me")
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_ssl_mode: str = "prefer"

    # ---- Redis ----
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # ---- JWT ----
    jwt_private_key: SecretStr = SecretStr("")
    jwt_public_key: str = ""
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 30
    jwt_issuer: str = "schoolerp.in"
    jwt_audience: str = "api"
    jwt_algorithm: str = "RS256"

    # ---- Encryption ----
    encryption_key: SecretStr = SecretStr("")

    # ---- Object Storage (S3 / MinIO) ----
    s3_endpoint_url: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: SecretStr = SecretStr("minioadmin")
    s3_bucket_name: str = "school-erp-dev"
    s3_region: str = "us-east-1"

    # ---- Google OAuth ----
    google_client_id: str = ""
    google_client_secret: SecretStr = SecretStr("")
    google_redirect_uri: str = "http://localhost:8000/api/v1/auth/google/callback"

    # ---- SMS ----
    sms_provider: str = "msg91"
    sms_api_key: SecretStr = SecretStr("")
    sms_sender_id: str = "SCHERP"

    # ---- Email ----
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: SecretStr = SecretStr("")
    email_from: str = "noreply@schoolerp.in"

    # ---- Firebase ----
    fcm_credentials_json: str = ""

    # ---- Razorpay ----
    razorpay_key_id: str = ""
    razorpay_key_secret: SecretStr = SecretStr("")
    razorpay_webhook_secret: SecretStr = SecretStr("")

    # ---- AI (optional) ----
    enable_ai_features: bool = False
    ai_api_key: SecretStr = SecretStr("")
    ai_model: str = ""

    # ---- Rate Limiting ----
    rate_limit_login: str = "10/minute"
    rate_limit_api_read: str = "300/minute"
    rate_limit_api_write: str = "60/minute"

    # ---- CORS ----
    cors_origins: list[str] = ["http://localhost:3000"]

    # ---- Logging ----
    log_level: str = "INFO"
    log_format: Literal["json", "console"] = "json"

    @property
    def database_url(self) -> str:
        """Async database URL for SQLAlchemy."""
        password = self.db_password.get_secret_value()
        return (
            f"postgresql+asyncpg://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def database_url_sync(self) -> str:
        """Sync database URL for Alembic migrations."""
        password = self.db_password.get_secret_value()
        return (
            f"postgresql://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @field_validator("app_secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if len(v) < 32 and v != "change-me-in-production":
            msg = "APP_SECRET_KEY must be at least 32 characters"
            raise ValueError(msg)
        return v


settings = Settings()
