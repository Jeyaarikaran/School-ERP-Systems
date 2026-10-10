from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.tenant import SchoolStatus


class SchoolCreate(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=20)
    domain: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)


class SchoolUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    domain: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    status: Optional[SchoolStatus] = None


class SchoolResponse(BaseModel):
    id: UUID
    name: str
    code: str
    status: SchoolStatus
    domain: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SchoolSettingsUpdate(BaseModel):
    timezone: Optional[str] = None
    currency: Optional[str] = None
    is_onboarding_complete: Optional[bool] = None
    features: Optional[Dict[str, Any]] = None


class SchoolSettingsResponse(BaseModel):
    id: UUID
    school_id: str
    timezone: str
    currency: str
    is_onboarding_complete: bool
    features: Dict[str, Any]

    class Config:
        from_attributes = True


class BranchCreate(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=20)
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)


class BranchUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    status: Optional[SchoolStatus] = None


class BranchResponse(BaseModel):
    id: UUID
    school_id: UUID
    name: str
    code: str
    address: Optional[str]
    city: Optional[str]
    district: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    status: SchoolStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
