"""Single source of truth for all system permissions."""

from dataclasses import dataclass

@dataclass(frozen=True)
class PermissionDef:
    name: str
    module: str
    description: str

# Defined for all phases, mapped exactly to the 05-role-permission-matrix
CATALOG = [
    # Students
    PermissionDef("students.create", "students", "Create/import students"),
    PermissionDef("students.view", "students", "View student data"),
    PermissionDef("students.view_sensitive", "students", "View medical/aadhaar data"),
    PermissionDef("students.update", "students", "Edit student records"),
    PermissionDef("students.delete", "students", "Archive students"),
    PermissionDef("students.export", "students", "Export student data"),
    # Guardians
    PermissionDef("guardians.view", "guardians", "View guardian data"),
    PermissionDef("guardians.manage", "guardians", "Manage guardians"),
    # Staff
    PermissionDef("staff.create", "staff", "Create staff records"),
    PermissionDef("staff.view", "staff", "View staff records"),
    PermissionDef("staff.update", "staff", "Edit staff records"),
    PermissionDef("staff.delete", "staff", "Archive staff records"),
    # Academic Structure
    PermissionDef("academic_years.manage", "academic", "Manage academic years"),
    PermissionDef("classes.manage", "academic", "Manage classes"),
    PermissionDef("sections.manage", "academic", "Manage sections"),
    PermissionDef("subjects.manage", "academic", "Manage subjects"),
    PermissionDef("assignments.manage", "academic", "Manage teacher assignments"),
    PermissionDef("electives.manage", "academic", "Manage student electives"),
    PermissionDef("enrollments.promote", "academic", "Run yearly promotion"),
    # Documents
    PermissionDef("documents.manage", "documents", "Manage student documents"),
    # Imports
    PermissionDef("imports.run", "imports", "Run bulk imports"),
    # Users
    PermissionDef("users.create", "users", "Create user accounts"),
    PermissionDef("users.view", "users", "View user data"),
    PermissionDef("users.update", "users", "Edit user profiles"),
    PermissionDef("users.deactivate", "users", "Deactivate users"),
    PermissionDef("users.assign_roles", "users", "Manage role assignments"),
    PermissionDef("users.reset_password", "users", "Send password reset links"),
    PermissionDef("users.manage_sessions", "users", "View/revoke user sessions"),
    # Roles
    PermissionDef("roles.view", "roles", "View roles and permissions"),
    PermissionDef("roles.manage", "roles", "Manage custom roles and permissions"),
    # Attendance & Calendar
    PermissionDef("attendance.view", "attendance", "View attendance"),
    PermissionDef("attendance.create", "attendance", "Submit attendance"),
    PermissionDef("attendance.update", "attendance", "Directly correct attendance"),
    PermissionDef("attendance.approve", "attendance", "Approve attendance corrections"),
    PermissionDef("attendance.export", "attendance", "Export attendance data"),
    PermissionDef("attendance.settings", "attendance", "Manage attendance settings"),
    PermissionDef("calendar.manage", "academic", "Manage school calendar and working days"),
    # Timetable
    PermissionDef("timetable.view", "timetable", "View timetables"),
    PermissionDef("timetable.manage", "timetable", "Manage and draft timetables"),
    PermissionDef("timetable.publish", "timetable", "Publish timetables"),
    # Curriculum
    PermissionDef("curriculum.view", "curriculum", "View curriculum syllabus and progress"),
    PermissionDef("curriculum.manage", "curriculum", "Manage syllabus structure"),
    PermissionDef("curriculum.update_progress", "curriculum", "Update completion progress"),
    # Homework
    PermissionDef("homework.view", "homework", "View homework assignments"),
    PermissionDef("homework.create", "homework", "Create homework"),
    PermissionDef("homework.update", "homework", "Edit homework details"),
    PermissionDef("homework.delete", "homework", "Archive homework"),
    PermissionDef("homework.submit", "homework", "Submit homework answers"),
    PermissionDef("homework.submit_for_child", "homework", "Submit homework on behalf of child"),
    PermissionDef("homework.evaluate", "homework", "Evaluate and grade homework"),
    # Grading
    PermissionDef("grading.manage", "grading", "Manage grading systems and bands"),
    # Exams
    PermissionDef("exams.view", "exams", "View exams"),
    PermissionDef("exams.manage", "exams", "Manage exam configuration"),
    PermissionDef("exams.schedule", "exams", "Manage exam schedules and invigilation"),
    PermissionDef("exams.analyze", "exams", "View exam analytics"),
    # Marks
    PermissionDef("marks.view", "marks", "View marks"),
    PermissionDef("marks.create", "marks", "Enter marks"),
    PermissionDef("marks.update", "marks", "Correct marks post-approval"),
    PermissionDef("marks.approve", "marks", "Approve mark sheets"),
    PermissionDef("marks.import", "marks", "Import marks"),
    # Results
    PermissionDef("results.view", "results", "View results"),
    PermissionDef("results.compute", "results", "Compute results"),
    PermissionDef("results.publish", "results", "Publish or unpublish results"),
    # Report Cards
    PermissionDef("report_cards.view", "report_cards", "View report cards"),
    PermissionDef("report_cards.generate", "report_cards", "Generate report cards"),
    PermissionDef("report_cards.remarks", "report_cards", "Enter report card remarks"),
    # Fees
    PermissionDef("fees.view", "fees", "View fee data"),
    PermissionDef("fees.structure_manage", "fees", "Manage fee structures and catalog"),
    PermissionDef("fees.assign", "fees", "Assign fees to students"),
    PermissionDef("fees.collect", "fees", "Collect counter payments"),
    PermissionDef("fees.pay", "fees", "Make online payments"),
    PermissionDef("fees.adjust_request", "fees", "Request fee adjustments (discounts)"),
    PermissionDef("fees.adjust_approve", "fees", "Approve standard fee adjustments"),
    PermissionDef("fees.adjust_approve_high", "fees", "Approve high-value fee adjustments"),
    PermissionDef("fees.void", "fees", "Void payments on the same day"),
    PermissionDef("fees.void_after_close", "fees", "Void payments after day closure"),
    PermissionDef("fees.refund_request", "fees", "Request fee refunds"),
    PermissionDef("fees.refund_approve", "fees", "Approve fee refunds"),
    PermissionDef("fees.refund_override", "fees", "Override refund limits and rules"),
    PermissionDef("fees.backdate", "fees", "Backdate fee collections"),
    PermissionDef("fees.day_close", "fees", "Close day book"),
    PermissionDef("fees.reopen_day", "fees", "Reopen closed day book"),
    PermissionDef("fees.report", "fees", "View financial reports"),
    PermissionDef("fees.export", "fees", "Export financial data"),
    PermissionDef("fees.gateway_manage", "fees", "Manage payment gateway settings"),
    PermissionDef("fees.credit_manage", "fees", "Manage student credit notes"),
    # Library
    PermissionDef("library.view", "library", "View catalog"),
    PermissionDef("library.view_own", "library", "View own library data"),
    PermissionDef("library.catalog_manage", "library", "Manage catalog"),
    PermissionDef("library.circulate", "library", "Issue/return/renew books"),
    PermissionDef("library.members_manage", "library", "Manage members"),
    PermissionDef("library.fines_manage", "library", "Manage fines"),
    PermissionDef("library.fines_waive", "library", "Waive fines"),
    PermissionDef("library.override_limits", "library", "Override circulation limits"),
    PermissionDef("library.stocktake", "library", "Manage stocktakes"),
    PermissionDef("library.report", "library", "View library reports"),
    PermissionDef("library.export", "library", "Export library data"),
    # Transport
    PermissionDef("transport.view", "transport", "View transport"),
    PermissionDef("transport.view_own", "transport", "View own transport data"),
    PermissionDef("transport.manage_assets", "transport", "Manage buses and crew"),
    PermissionDef("transport.manage_routes", "transport", "Manage stops and routes"),
    PermissionDef("transport.assign_students", "transport", "Assign students to routes"),
    PermissionDef("transport.view_manifest", "transport", "View manifests"),
    PermissionDef("transport.view_sensitive", "transport", "View full license numbers"),
    PermissionDef("transport.override_compliance", "transport", "Override compliance expiry"),
    PermissionDef("transport.run_trips", "transport", "Run trips (driver/attendant)"),
    PermissionDef("transport.announce", "transport", "Send transport announcements"),
    PermissionDef("transport.report", "transport", "View transport reports"),
    PermissionDef("transport.export", "transport", "Export transport data"),
    # Notifications
    PermissionDef("notifications.view", "notifications", "View notifications"),
    PermissionDef("notifications.send", "notifications", "Send manual notifications"),
    PermissionDef("notifications.templates_manage", "notifications", "Manage templates"),
    PermissionDef("notifications.rules_manage", "notifications", "Manage rules"),
    PermissionDef("notifications.logs_view", "notifications", "View delivery logs"),
    PermissionDef("emergency.send", "notifications", "Send emergency alerts"),
    PermissionDef("devices.manage_own", "notifications", "Manage own devices"),
    # Announcements
    PermissionDef("announcements.view", "announcements", "View announcements"),
    PermissionDef("announcements.create", "announcements", "Create announcements"),
    PermissionDef("announcements.publish_school", "announcements", "Publish to entire school"),
    PermissionDef("announcements.approve", "announcements", "Approve announcements"),
    # Leave
    PermissionDef("leave.request", "leave", "Submit leave requests"),
    PermissionDef("leave.view", "leave", "View own leave requests"),
    PermissionDef("leave.approve", "leave", "Approve/reject leave"),
    PermissionDef("leave.cancel_approved", "leave", "Cancel approved leave"),
    PermissionDef("leave.manage_types", "leave", "Manage leave types"),
    PermissionDef("leave.view_all", "leave", "View all leave requests"),
    # Substitutions
    PermissionDef("substitutions.view", "substitutions", "View substitutions"),
    PermissionDef("substitutions.manage", "substitutions", "Manage substitutions"),
    # Reports
    PermissionDef("reports.generate", "reports", "Generate reports"),
    PermissionDef("reports.view", "reports", "View reports"),
    PermissionDef("reports.view_all", "reports", "View all reports"),
    PermissionDef("reports.export", "reports", "Export reports"),
    PermissionDef("reports.schedule", "reports", "Schedule reports"),
    # Dashboards
    PermissionDef("dashboards.view", "dashboards", "View dashboards"),
    # Insights
    PermissionDef("insights.view_at_risk", "insights", "View at-risk students"),
    # Privacy
    PermissionDef("privacy.view", "privacy", "View privacy settings"),
    PermissionDef("privacy.manage", "privacy", "Manage privacy policies"),
    PermissionDef("privacy.requests_view", "privacy", "View data requests"),
    PermissionDef("privacy.requests_manage", "privacy", "Manage data requests"),
    PermissionDef("privacy.erasure_approve", "privacy", "Approve data erasure"),
    # AI
    PermissionDef("ai.manage_settings", "ai", "Manage AI settings and toggles"),
    PermissionDef("ai.use_question_generator", "ai", "Use AI question generator"),
    PermissionDef("ai.approve_drafts", "ai", "Approve AI drafts"),
    # Settings
    PermissionDef("settings.view", "settings", "View settings"),
    PermissionDef("settings.update", "settings", "Update settings"),
    # Messages
    PermissionDef("messages.send", "messages", "Send messages"),
    PermissionDef("messages.view", "messages", "View messages"),
    PermissionDef("messages.moderate", "messages", "Moderate messages"),
    # Audit
    PermissionDef("audit.view", "audit", "View audit logs"),
]
