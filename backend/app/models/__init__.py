"""SQLAlchemy models export."""

from app.models.tenant import School, SchoolSettings, SystemSettings
from app.models.identity import User, UserSession, RefreshToken, OTPCode, TwoFactorSecret, TwoFactorRecoveryCode, UserIdentity
from app.models.rbac import Role, Permission, RolePermission, UserRole
from app.models.audit import AuditLog, IdempotencyKey
from app.models.academic import AcademicYear, ClassLevel, Room, Section, Subject, ClassSubject, CodeCounter
from app.models.people import Student, Guardian, StudentGuardian, StudentEnrollment, StudentStatusHistory, Staff, Teacher, TeacherSubject
from app.models.storage import FileMetadata, Document, ImportJob
from app.models.attendance import (
    SchoolCalendarDay, AttendanceSession, AttendanceRecord, AttendanceCorrection,
    AttendanceHistory, AttendanceSyncOp, AttendanceDailySummary, OutboxEvent
)
from app.models.timetable import BellSchedule, BellSchedulePeriod, BellScheduleDay, Timetable, TimetableEntry, TimetableSlotClaim
from app.models.curriculum import CurriculumUnit, CurriculumProgress, CurriculumProgressHistory
from app.models.homework import Homework, HomeworkTarget, HomeworkAttachment, HomeworkSubmission, HomeworkSubmissionAttempt, HomeworkSubmissionFile
from app.models.exams import (
    GradingSystem, GradeBand, ExamType, Exam, ExamClass, ExamSubject, ExamComponent,
    StudentSubjectEnrollment, ExamSchedule, ExamInvigilation, MarkSheet, Mark, MarksHistory,
    ExamSubjectResult, ExamResult, ReportPeriod, ReportPeriodExam, ReportCardRemark, ReportCard
)
from app.models.fees import (
    FeeCategory, FeeStructure, FeeStructureClass, FeeStructureItem, FeeInstallment, LateFeeRule,
    AdjustmentTemplate, StudentAdjustment, StudentFeeItem, FeeLedgerEntry, FeePayment,
    PaymentAllocation, FeeReceipt, ReceiptCounter, FeeRefund, WebhookEvent, FeeDayClosure
)
from app.models.notifications import (
    NotificationTemplate, NotificationRule, Notification, NotificationDelivery,
    NotificationPreference, DeviceToken, Suppression, MessagingUsage
)
from app.models.announcements import Announcement, AnnouncementRecipient
from app.models.messaging import Conversation, ConversationParticipant, Message, MessageReport
from app.models.leave import LeaveType, LeaveEntitlement, LeaveRequest, LeaveApproval
from app.models.substitutions import SubstitutionNeed, TimetableSubstitution
from app.models.library import (
    LibraryCategory, LibraryBook, LibraryCopy, LibraryMember, BookIssue,
    LibraryCirculationEvent, LibraryFine, LibraryStocktake, LibraryStocktakeScan
)
from app.models.transport import (
    TransportBus, TransportCrewProfile, TransportBusCrew, TransportFeeZone,
    TransportFeePlan, TransportStop, TransportRoute, TransportRouteStop,
    TransportRouteAssignment, StudentTransport, TransportTripRun, TransportBoardingEvent
)
from app.models.analytics import (
    AnalyticsAttendanceDaily, AnalyticsAttendanceStudentMonth,
    AnalyticsExamSubjectStats, AnalyticsExamStudentTrend,
    AnalyticsFeeDaily, AnalyticsFeeDuesSnapshot,
    AnalyticsHomeworkSectionWeek, AnalyticsCurriculumSectionSubject,
    AnalyticsLibraryDaily, AnalyticsTransportDaily,
    AnalyticsEngagementDaily, AnalyticsTeacherWorkload,
    RollupRun, StudentRiskScore
)
from app.models.reports import (
    ReportJob, ReportSchedule
)
from app.models.privacy import (
    Consent, PolicyDocument, PolicyAcceptance, DataRequest, RetentionPolicy
)
from app.models.ai import (
    AIFeatureToggle, AIJob, AIUsageLog, AIDraft
)

__all__ = [
    "School",
    "SchoolSettings",
    "SystemSettings",
    "User",
    "UserSession",
    "RefreshToken",
    "OTPCode",
    "TwoFactorSecret",
    "TwoFactorRecoveryCode",
    "Role",
    "Permission",
    "RolePermission",
    "UserRole",
    "AuditLog",
    "IdempotencyKey",
    # Academic
    "AcademicYear",
    "ClassLevel",
    "Room",
    "Section",
    "Subject",
    "ClassSubject",
    "CodeCounter",
    # People
    "Student",
    "Guardian",
    "StudentGuardian",
    "StudentEnrollment",
    "StudentStatusHistory",
    "Staff",
    "Teacher",
    "TeacherSubject",
    # Storage
    "FileMetadata",
    "Document",
    "ImportJob",
    # Attendance & Core
    "SchoolCalendarDay",
    "AttendanceSession",
    "AttendanceRecord",
    "AttendanceCorrection",
    "AttendanceHistory",
    "AttendanceSyncOp",
    "AttendanceDailySummary",
    "OutboxEvent",
    # Timetable
    "BellSchedule",
    "BellSchedulePeriod",
    "BellScheduleDay",
    "Timetable",
    "TimetableEntry",
    "TimetableSlotClaim",
    # Curriculum
    "CurriculumUnit",
    "CurriculumProgress",
    "CurriculumProgressHistory",
    # Homework
    "Homework",
    "HomeworkTarget",
    "HomeworkAttachment",
    "HomeworkSubmission",
    "HomeworkSubmissionAttempt",
    "HomeworkSubmissionFile",
    # Exams & Results
    "GradingSystem",
    "GradeBand",
    "ExamType",
    "Exam",
    "ExamClass",
    "ExamSubject",
    "ExamComponent",
    "StudentSubjectEnrollment",
    "ExamSchedule",
    "ExamInvigilation",
    "MarkSheet",
    "Mark",
    "MarksHistory",
    "ExamSubjectResult",
    "ExamResult",
    "ReportPeriod",
    "ReportPeriodExam",
    "ReportCardRemark",
    "ReportCard",
    # Fees & Payments
    "FeeCategory",
    "FeeStructure",
    "FeeStructureClass",
    "FeeStructureItem",
    "FeeInstallment",
    "LateFeeRule",
    "AdjustmentTemplate",
    "StudentAdjustment",
    "StudentFeeItem",
    "FeeLedgerEntry",
    "FeePayment",
    "PaymentAllocation",
    "FeeReceipt",
    "ReceiptCounter",
    "FeeRefund",
    "WebhookEvent",
    "FeeDayClosure",
    "UserIdentity",
    # Notifications & Communications
    "NotificationTemplate",
    "NotificationRule",
    "Notification",
    "NotificationDelivery",
    "NotificationPreference",
    "DeviceToken",
    "Suppression",
    "MessagingUsage",
    "Announcement",
    "AnnouncementRecipient",
    "Conversation",
    "ConversationParticipant",
    "Message",
    "MessageReport",
    # Leave & Substitutions
    "LeaveType",
    "LeaveEntitlement",
    "LeaveRequest",
    "LeaveApproval",
    "SubstitutionNeed",
    "TimetableSubstitution",
    # Library
    "LibraryCategory",
    "LibraryBook",
    "LibraryCopy",
    "LibraryMember",
    "BookIssue",
    "LibraryCirculationEvent",
    "LibraryFine",
    "LibraryStocktake",
    "LibraryStocktakeScan",
    # Transport
    "TransportBus",
    "TransportCrewProfile",
    "TransportBusCrew",
    "TransportFeeZone",
    "TransportFeePlan",
    "TransportStop",
    "TransportRoute",
    "TransportRouteStop",
    "TransportRouteAssignment",
    "StudentTransport",
    "TransportTripRun",
    "TransportBoardingEvent",
    # Analytics
    "AnalyticsAttendanceDaily",
    "AnalyticsAttendanceStudentMonth",
    "AnalyticsExamSubjectStats",
    "AnalyticsExamStudentTrend",
    "AnalyticsFeeDaily",
    "AnalyticsFeeDuesSnapshot",
    "AnalyticsHomeworkSectionWeek",
    "AnalyticsCurriculumSectionSubject",
    "AnalyticsLibraryDaily",
    "AnalyticsTransportDaily",
    "AnalyticsEngagementDaily",
    "AnalyticsTeacherWorkload",
    "RollupRun",
    "StudentRiskScore",
    # Reports
    "ReportJob",
    "ReportSchedule",
    # Privacy
    "Consent",
    "PolicyDocument",
    "PolicyAcceptance",
    "DataRequest",
    "RetentionPolicy",
    # AI
    "AIFeatureToggle",
    "AIJob",
    "AIUsageLog",
    "AIDraft",
]
