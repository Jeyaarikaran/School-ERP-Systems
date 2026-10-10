from app.schemas.auth import LoginRequest, LoginResponse, TokenRefreshRequest, ForgotPasswordRequest, ResetPasswordRequest, OTPRequest, OTPVerifyRequest, UserProfileResponse
from app.schemas.user import UserCreate, UserResponse, RoleCreate, RoleResponse, PermissionResponse
from app.schemas.academic import AcademicYearCreate, AcademicYearResponse, SectionCreate, SectionResponse
from app.schemas.attendance import AttendanceSubmitRequest, AttendanceRecordResponse, AttendanceSessionResponse, SyncBatchRequest, SyncBatchResponse
from app.schemas.people import StudentCreate, StudentResponse, GuardianCreate, GuardianResponse, StaffCreate, StaffResponse, TeacherCreate, TeacherResponse

__all__ = [
    "LoginRequest", "LoginResponse", "TokenRefreshRequest", "ForgotPasswordRequest", "ResetPasswordRequest", "OTPRequest", "OTPVerifyRequest", "UserProfileResponse",
    "UserCreate", "UserResponse", "RoleCreate", "RoleResponse", "PermissionResponse",
    "AcademicYearCreate", "AcademicYearResponse", "SectionCreate", "SectionResponse",
    "AttendanceSubmitRequest", "AttendanceRecordResponse", "AttendanceSessionResponse", "SyncBatchRequest", "SyncBatchResponse",
    "StudentCreate", "StudentResponse", "GuardianCreate", "GuardianResponse", "StaffCreate", "StaffResponse", "TeacherCreate", "TeacherResponse"
]
