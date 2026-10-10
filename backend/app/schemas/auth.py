"""Authentication and Identity Pydantic schemas."""

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime


class LoginRequest(BaseModel):
    school_code: str | None = None
    identifier: str  # email or phone
    password: str
    device_name: str | None = None
    user_agent: str | None = None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    requires_2fa: bool = False
    user: dict


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    school_code: str | None = None
    identifier: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=10)


class OTPRequest(BaseModel):
    school_code: str | None = None
    phone: str


class OTPVerifyRequest(BaseModel):
    phone: str
    code: str


class SessionResponse(BaseModel):
    id: UUID
    device_name: str | None
    ip_address: str | None
    user_agent: str | None
    last_seen_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr | None
    phone: str | None
    status: str
    roles: list[str]
    permissions: list[str]
    school_id: UUID | None
    
    class Config:
        from_attributes = True
