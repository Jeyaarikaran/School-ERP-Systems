from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

from app.core.config import settings

# Argon2id — configured per Security docs (100-200ms target)
_ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=2,
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against Argon2id hash."""
    try:
        return _ph.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def get_password_hash(password: str) -> str:
    """Hash password with Argon2id."""
    return _ph.hash(password)


def get_dummy_hash() -> str:
    """Return a dummy hash to prevent timing attacks on unknown users."""
    return _ph.hash("dummy_password_for_timing_attack_prevention")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a short-lived access JWT using RS256."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    to_encode.update({"exp": expire, "iss": settings.jwt_issuer, "aud": settings.jwt_audience})
    private_key = settings.jwt_private_key.get_secret_value().replace("\\n", "\n")
    return jwt.encode(to_encode, private_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT access token."""
    public_key = settings.jwt_public_key.replace("\\n", "\n")
    return jwt.decode(
        token,
        public_key,
        algorithms=[settings.jwt_algorithm],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )
