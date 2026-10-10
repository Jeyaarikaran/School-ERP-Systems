"""Dependencies for authentication and RBAC enforcement."""

from typing import Annotated
from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from app.core.config import settings
from app.core.errors import AuthenticationError, AuthorizationError, TokenExpiredError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.models import identity
from sqlalchemy import select

bearer_scheme = HTTPBearer(auto_error=False)


async def get_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Validate JWT and return payload. Rejects if session is revoked."""
    if not credentials:
        raise AuthenticationError("Missing token")

    try:
        public_key = settings.jwt_public_key.replace("\\n", "\n")
        payload = jwt.decode(
            credentials.credentials,
            public_key,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")

    # Check revocation in DB
    session_id = payload.get("sid")
    if not session_id:
        raise AuthenticationError("Invalid session")
        
    stmt = select(identity.UserSession.revoked_at).where(identity.UserSession.id == session_id)
    result = await db.execute(stmt)
    revoked_at = result.scalar()
    
    if revoked_at is not None:
        raise AuthenticationError("Session revoked")
        
    request.state.user = payload
    return payload


def require_permission(permission: str):
    """Dependency that enforces a single permission."""
    async def _check(payload: dict = Depends(get_token_payload)):
        roles = payload.get("roles", [])
        if "super_admin" in roles:
            return payload
            
        # In a full implementation, we'd resolve user permissions from Redis cache
        # For this scaffold, we check if the requested permission is in the token's resolved list
        # (Assuming the token payload actually carries resolved permissions for simplicity in Phase 2)
        token_perms = payload.get("permissions", [])
        if permission not in token_perms:
            raise AuthorizationError(f"Missing required permission: {permission}")
            
        return payload
    return _check
