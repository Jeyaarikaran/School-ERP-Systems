# Notification Event Catalog

This catalog documents the valid outbox events, their expected payloads, and the default routing rules in the system.

## Core App Events (Phases 1-7)
- `attendance.student_absent`: Triggered when a student is marked absent.
- `fee.payment_captured`: Triggered when a fee payment is successfully processed.

## Phase 8: Messaging & Leave
- `message.received`: Direct message received.
- `leave.requested`: Staff/Student submitted leave.
- `leave.approved`: Leave request approved.
- `leave.rejected`: Leave request rejected.
- `announcement.published`: A new announcement was published to a target audience.

## Phase 9: Library
- `library.issued`: Book issued to member. (Recipients: student/guardian or staff)
- `library.returned`: Book returned. (Recipients: student/guardian or staff)
- `library.fine_assessed`: Overdue or damage fine assessed.
- `library.fine_waived`: Fine waived by librarian.
- `library.due_soon`: Book due in 2 days. (Job generated, deduplicated)
- `library.overdue`: Book overdue by 1 or 7 days. (Job generated, deduplicated)

## Phase 9: Transport
- `transport.trip_started`: Driver started the trip run.
- `transport.trip_delayed`: Delay announced for the trip run.
- `transport.trip_cancelled`: Trip run cancelled.
- `transport.boarded`: Student boarded the bus. (Opt-in by school default: OFF)
- `transport.alighted`: Student alighted the bus. (Opt-in by school default: OFF)
- `transport.assignment_changed`: Student transport enrollment changed or stopped.
- `transport.document_expiring`: Bus or crew compliance document is expiring (30, 7, 0 days). (Recipients: Transport Admin)
