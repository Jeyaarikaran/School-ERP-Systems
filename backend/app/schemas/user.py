"""User and Role Pydantic schemas."""

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role_ids: list[UUID]


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str | None
    phone: str | None
    status: str
    last_login_at: datetime | None

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str
    description: str | None = None
    permission_ids: list[UUID]


class RoleResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    is_system: bool

    class Config:
        from_attributes = True


class PermissionResponse(BaseModel):
    id: UUID
    name: str
    module: str
    description: str | None

    class Config:
        from_attributes = True
