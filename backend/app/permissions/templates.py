"""Default role templates mapped to permissions."""

from app.permissions.catalog import CATALOG

def _expand(patterns: list[str]) -> list[str]:
    """Expand wildcard patterns like 'students.*' into concrete permission names."""
    result = set()
    for p in patterns:
        if p.endswith(".*"):
            module = p.split(".")[0]
            result.update(perm.name for perm in CATALOG if perm.module == module)
        elif p == "*":
            result.update(perm.name for perm in CATALOG)
        else:
            result.add(p)
    return list(result)

# The base templates for the 10 system roles. Super admin is implicit in code.
SYSTEM_ROLES = {
    "school_admin": _expand([
        "students.*", "users.*", "roles.*", "attendance.*", "timetable.*",
        "staff.*", "guardians.*", "academic_years.*", "classes.*", "sections.*",
        "subjects.*", "assignments.manage", "electives.manage", "enrollments.promote", "imports.run",
        "documents.manage", "calendar.manage",
        "homework.*", "curriculum.*",
        "grading.*", "exams.*", "marks.*", "results.*", "report_cards.*", "fees.*",
        "library.*",
        "transport.*", "notifications.*", "emergency.send", "devices.manage_own",
        "announcements.*",
        "leave.*", "substitutions.*",
        "messages.*", "reports.*", "settings.*", "audit.view",
    ]),
    "principal": _expand([
        "students.view", "students.view_sensitive", "students.export",
        "users.view",
        "attendance.view", "attendance.update", "attendance.approve", "attendance.export",
        "timetable.view", "curriculum.*",
        "homework.view", "exams.*", "marks.view", "marks.approve", "results.*", "report_cards.*",
        "fees.view", "fees.report", "fees.adjust_approve", "fees.adjust_approve_high", "fees.refund_approve",
        "library.view", "library.report", "transport.view", "transport.report",
        "notifications.*", "emergency.send", "devices.manage_own",
        "announcements.*",
        "leave.request", "leave.view", "leave.approve", "leave.cancel_approved", "leave.view_all",
        "substitutions.*",
        "messages.*", "reports.*", "settings.view", "audit.view",
    ]),
    "teacher": _expand([
        "students.view",
        "attendance.create", "attendance.view", "attendance.update", "attendance.export",
        "timetable.view",
        "homework.create", "homework.view", "homework.evaluate", "curriculum.view", "curriculum.update_progress",
        "exams.view", "marks.view", "marks.create", "marks.update", "results.view", "report_cards.view", "report_cards.remarks",
        "library.view", "library.view_own",
        "notifications.view", "notifications.send", "devices.manage_own",
        "announcements.view", "announcements.create",
        "leave.request", "leave.view",
        "substitutions.view",
        "messages.send", "messages.view", "reports.view",
    ]),
    "parent": _expand([
        "students.view", "attendance.view", "timetable.view", "homework.view", "homework.submit_for_child", "curriculum.view",
        "exams.view", "results.view", "report_cards.view", "fees.view", "fees.pay", "transport.view", "transport.view_own",
        "notifications.view", "devices.manage_own", "announcements.view",
        "leave.request", "leave.view",
        "messages.send", "messages.view",
    ]),
    "student": _expand([
        "students.view", "attendance.view", "timetable.view", "homework.view", "homework.submit", "curriculum.view",
        "exams.view", "results.view", "report_cards.view", "fees.view", "library.view", "library.view_own", "transport.view", "transport.view_own",
        "notifications.view", "devices.manage_own", "announcements.view",
        "leave.request", "leave.view",
        "messages.send", "messages.view",
    ]),
    "accountant": _expand([
        "students.view", "notifications.view",
        "fees.view", "fees.collect", "fees.adjust_request", "fees.refund_request", "fees.void", "fees.day_close", "fees.report", "fees.export",
        "leave.request", "leave.view", "messages.send", "messages.view", "reports.*",
    ]),
    "librarian": _expand([
        "library.*", "notifications.view", "leave.request", "leave.view", "messages.send", "messages.view",
    ]),
    "transport_admin": _expand([
        "transport.*", "notifications.view", "leave.request", "leave.view", "messages.send", "messages.view",
    ]),
    "receptionist": _expand([
        "students.create", "students.view", "students.update",
        "notifications.view", "leave.request", "leave.view", "messages.send", "messages.view",
    ]),
    "driver_attendant": _expand([
        "transport.view_manifest", "transport.run_trips", "transport.announce",
        "notifications.view", "leave.request", "leave.view", "messages.send", "messages.view",
    ]),
}
