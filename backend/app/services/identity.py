import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.models.tenant import School
from app.models.identity import User, UserSession, RefreshToken
from app.models.rbac import UserRole, RolePermission, Permission, Role
from app.core.security import verify_password, get_dummy_hash, create_access_token
from app.core.config import settings

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _resolve_user_roles_and_permissions(self, user_id: str) -> tuple[list[str], list[str]]:
        """Resolve all roles and distinct permissions for a user."""
        # 1. Fetch User Roles
        stmt = select(Role).join(UserRole).where(UserRole.user_id == user_id)
        result = await self.db.execute(stmt)
        roles = result.scalars().all()
        role_names = [r.name for r in roles]

        if not roles:
            return [], []

        # 2. Fetch Permissions for those roles
        role_ids = [r.id for r in roles]
        perm_stmt = select(Permission.name).join(RolePermission).where(RolePermission.role_id.in_(role_ids))
        perm_result = await self.db.execute(perm_stmt)
        permissions = list(set(perm_result.scalars().all()))

        return role_names, permissions

    async def _create_session_and_tokens(self, user: User, school_id: str, device_name: str | None, user_agent: str | None, ip_address: str | None) -> dict:
        # Resolve RBAC
        role_names, permissions = await self._resolve_user_roles_and_permissions(str(user.id))

        # Create Session in DB
        session = UserSession(
            user_id=user.id,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent
        )
        self.db.add(session)
        await self.db.flush()  # to get session.id

        # Generate Access Token
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "school_id": school_id,
                "sid": str(session.id),
                "roles": role_names,
                "permissions": permissions,
                "typ": "Bearer"
            }
        )

        # Generate Refresh Token
        refresh_token_str = secrets.token_hex(32)
        family_id = secrets.token_hex(16)
        
        # In a real app we'd hash the refresh token. For phase 2 demo, we can store it directly or hashed.
        refresh_token_record = RefreshToken(
            session_id=session.id,
            family_id=family_id,
            token_hash=refresh_token_str, # Normally hashed
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_token_expire_days)
        )
        self.db.add(refresh_token_record)
        
        # Update last login
        user.last_login_at = datetime.now(timezone.utc)
        user.failed_login_count = 0
        user.locked_until = None
        
        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str,
            "token_type": "bearer",
            "expires_in": settings.jwt_access_token_expire_minutes * 60,
            "user": {
                "id": str(user.id),
                "school_id": school_id,
                "email": user.email,
                "full_name": user.full_name,
                "status": user.status,
                "roles": role_names,
                "permissions": permissions,
            }
        }

    async def authenticate_user(
        self, 
        identifier: str, 
        password: str, 
        school_code: str | None,
        device_name: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None
    ) -> dict | None:
        """Authenticate and create session."""
        
        school_id = None
        if school_code:
            stmt = select(School).where(School.code == school_code, School.status == 'active')
            result = await self.db.execute(stmt)
            school = result.scalars().first()
            if not school:
                get_dummy_hash()
                return None
            school_id = str(school.id)

        # Resolve User (Identifier = email or phone)
        user_stmt = select(User).where(
            (User.email == identifier) | (User.phone == identifier),
            User.status.in_(['invited', 'active'])
        )
        if school_id:
            user_stmt = user_stmt.where(User.school_id == school_id)
            
        result = await self.db.execute(user_stmt)
        user = result.scalars().first()

        if not user or not user.password_hash:
            get_dummy_hash()
            return None
            
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            return None # Locked out

        # Verify Password
        if not verify_password(password, user.password_hash):
            user.failed_login_count += 1
            if user.failed_login_count >= 5:
                user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
            await self.db.commit()
            return None

        # Success!
        return await self._create_session_and_tokens(user, school_id or str(user.school_id), device_name, user_agent, ip_address)


    async def logout(self, session_id: str) -> None:
        """Revoke a specific session."""
        stmt = update(UserSession).where(UserSession.id == session_id).values(
            revoked_at=datetime.now(timezone.utc),
            revoked_reason="user_logout"
        )
        await self.db.execute(stmt)
        await self.db.commit()
        
    async def logout_all(self, user_id: str, current_session_id: str) -> None:
        """Revoke all sessions for a user EXCEPT the current one."""
        stmt = update(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.id != current_session_id,
            UserSession.revoked_at.is_(None)
        ).values(
            revoked_at=datetime.now(timezone.utc),
            revoked_reason="logout_all_devices"
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_active_sessions(self, user_id: str):
        stmt = select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.revoked_at.is_(None)
        ).order_by(UserSession.last_seen_at.desc())
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
