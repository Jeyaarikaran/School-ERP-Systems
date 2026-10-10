from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.schemas.auth import LoginRequest, LoginResponse, UserProfileResponse, SessionResponse
from app.services.identity import AuthService
from app.permissions.dependencies import get_token_payload

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, req: Request, db: AsyncSession = Depends(get_db_session)):
    """Authenticate a user and return JWT tokens."""
    auth_service = AuthService(db)
    
    # Use client IP from request
    ip_address = req.client.host if req.client else None
    
    tokens = await auth_service.authenticate_user(
        identifier=request.identifier, 
        password=request.password, 
        school_code=request.school_code,
        device_name=request.device_name,
        user_agent=request.user_agent or req.headers.get("user-agent"),
        ip_address=ip_address
    )
    if not tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return tokens


@router.post("/logout")
async def logout(
    payload: dict = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db_session)
):
    """Logout current session."""
    auth_service = AuthService(db)
    session_id = payload.get("sid")
    if session_id:
        await auth_service.logout(session_id)
    return {"status": "logged_out"}


@router.post("/logout-all")
async def logout_all(
    payload: dict = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db_session)
):
    """Logout all devices EXCEPT current session."""
    auth_service = AuthService(db)
    user_id = payload.get("sub")
    session_id = payload.get("sid")
    
    if user_id and session_id:
        await auth_service.logout_all(user_id, session_id)
    return {"status": "all_other_devices_logged_out"}


@router.get("/sessions", response_model=list[SessionResponse])
async def list_sessions(
    payload: dict = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db_session)
):
    """List all active sessions for the current user."""
    auth_service = AuthService(db)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    return await auth_service.get_active_sessions(user_id)


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db_session)
):
    """Get profile and permissions for the current user."""
    from sqlalchemy import select
    from app.models.identity import User
    
    user_id = payload.get("sub")
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "status": user.status,
        "roles": payload.get("roles", []),
        "permissions": payload.get("permissions", []),
        "school_id": user.school_id
    }
