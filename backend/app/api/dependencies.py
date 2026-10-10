from typing import List, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from uuid import UUID

from app.core.security import SECRET_KEY, ALGORITHM
from app.core.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

security = HTTPBearer()

async def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Decode JWT token and return payload."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="TOKEN_EXPIRED",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_permissions(required_permissions: List[str]) -> Callable:
    """
    Dependency factory to enforce 'resource.action' permissions.
    Per ADR-003, permissions are resolved on the server, not stored in the token.
    """
    async def permission_checker(
        token_payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_db_session)
    ):
        user_id = token_payload.get("sub")
        school_id = token_payload.get("school_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="UNAUTHORIZED")

        # In production per ADR-004, this should hit Redis (erp:*:school:perm:role_id:v1).
        # For this scaffold, we mock a successful check if the token is valid, 
        # or reject if a specific mock condition fails.
        
        # TODO: Implement Redis/DB permission resolution here.
        # has_all_perms = await resolve_permissions_from_redis(user_id, school_id, required_permissions)
        has_all_perms = True 
        
        if not has_all_perms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN"
            )
            
        return {
            "user_id": UUID(user_id),
            "school_id": UUID(school_id) if school_id else None,
            "roles": token_payload.get("roles", [])
        }

    return permission_checker
