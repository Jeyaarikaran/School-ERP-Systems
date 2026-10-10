# 05 — Role × Permission Matrix

> **Version:** 1.0 | **Phase:** 1 | **Status:** Approved (pending gate)

---

## Table of Contents

1. [Role Definitions](#1-role-definitions)
2. [Permission Registry](#2-permission-registry)
3. [Role × Permission Matrix](#3-role--permission-matrix)
4. [Row-Level Scope Rules](#4-row-level-scope-rules)
5. [Role Hierarchy & Escalation Rules](#5-role-hierarchy--escalation-rules)
6. [Seed Data](#6-seed-data)
7. [Assumptions and Open Questions](#7-assumptions-and-open-questions)

---

## 1. Role Definitions

| Role | Slug | Scope | Description |
|---|---|---|---|
| Super Admin | `super_admin` | Platform-wide | Platform operator; manages all schools, system settings, audit. Not tied to a single school. |
| School Admin | `school_admin` | Single school | Full school management — students, staff, academics, fees, settings, reports. |
| Principal | `principal` | Single school | Read-heavy oversight of all school data; can approve marks, attendance corrections, leave. |
| Teacher | `teacher` | Single school | Attendance, homework, marks for assigned sections/subjects. View timetable, leave requests. |
| Parent | `parent` | Single school | View linked children's data — attendance, marks, fees, homework, timetable. Pay fees. |
| Student | `student` | Single school | View own records — attendance, marks, timetable, homework, library. |
| Accountant | `accountant` | Single school | Fee structures, payments, receipts, refunds, financial reports. |
| Librarian | `librarian` | Single school | Book catalog, issue/return, fines, library reports. |
| Transport Admin | `transport_admin` | Single school | Routes, stops, buses, drivers, student transport assignments. |
| Receptionist | `receptionist` | Single school | Student intake, visitor log, basic student search, document upload. |

> **Note:** A user can have multiple roles (e.g., a teacher who is also a transport_admin). Permissions are the union of all assigned roles.

---

## 2. Permission Registry

Permissions follow `{module}.{action}` naming. All permissions are seeded in the `permissions` table.

### 2.1 Students Module

| Permission | Description |
|---|---|
| `students.create` | Admit new students, bulk import |
| `students.view` | View student list, detail, enrollment history |
| `students.view_sensitive` | View medical notes, aadhaar info |
| `students.update` | Edit student records, link guardians |
| `students.delete` | Archive/soft-delete students |
| `students.export` | Export student data to CSV/Excel |

### 2.2 Users Module

| Permission | Description |
|---|---|
| `users.create` | Create staff/teacher/parent accounts |
| `users.view` | View user list and details |
| `users.update` | Edit user profiles, status changes |
| `users.delete` | Deactivate/archive user accounts |
| `users.assign_role` | Assign or remove roles from users |

### 2.3 Attendance Module

| Permission | Description |
|---|---|
| `attendance.create` | Submit attendance for a session |
| `attendance.view` | View attendance records and reports |
| `attendance.correct` | Submit and approve attendance corrections |
| `attendance.lock` | Lock attendance session (prevent further edits) |
| `attendance.report` | Generate attendance reports (section/school-wide) |

### 2.4 Timetable Module

| Permission | Description |
|---|---|
| `timetable.create` | Create and edit timetables, periods, entries |
| `timetable.view` | View timetables |
| `timetable.publish` | Publish timetable (makes it visible to all) |

### 2.5 Homework Module

| Permission | Description |
|---|---|
| `homework.create` | Create, edit, delete homework |
| `homework.view` | View homework list and details |
| `homework.submit` | Submit homework (student) |
| `homework.grade` | Grade and return homework submissions |

### 2.6 Exams Module

| Permission | Description |
|---|---|
| `exams.create` | Create/edit exams, subjects, schedules |
| `exams.view` | View exams and schedules |
| `exams.enter_marks` | Enter/update marks for exam subjects |
| `exams.approve_marks` | Approve/verify marks before publish |
| `exams.publish` | Publish exam results (triggers notifications) |
| `exams.report` | Generate exam/marks reports, rank lists |

### 2.7 Fees Module

| Permission | Description |
|---|---|
| `fees.view` | View fee structures, student fees, payments |
| `fees.create_structure` | Create/edit fee categories, structures, installments |
| `fees.collect` | Record cash/cheque payments |
| `fees.pay` | Create online payment order (parent self-service) |
| `fees.refund` | Initiate refund |
| `fees.waive` | Apply discount or waiver |
| `fees.report` | Financial reports, collection summary, defaulter list |

### 2.8 Library Module

| Permission | Description |
|---|---|
| `library.view` | Search and view books, categories |
| `library.manage_books` | Add/edit/delete books and copies |
| `library.issue` | Issue books to users |
| `library.return` | Process book returns |
| `library.manage_fines` | Create, waive, mark fines as paid |

### 2.9 Transport Module

| Permission | Description |
|---|---|
| `transport.view` | View routes, stops, buses, assignments |
| `transport.manage` | Create/edit routes, stops, buses, drivers |
| `transport.assign` | Assign students to transport routes/stops |

### 2.10 Notifications Module

| Permission | Description |
|---|---|
| `notifications.view` | View own notifications |
| `notifications.send` | Send broadcast notifications |
| `notifications.manage_templates` | Create/edit notification templates |

### 2.11 Leave Module

| Permission | Description |
|---|---|
| `leave.create` | Submit own leave request |
| `leave.view` | View leave requests (scoped) |
| `leave.approve` | Approve/reject leave requests |

### 2.12 Reports Module

| Permission | Description |
|---|---|
| `reports.generate` | Trigger async report generation |
| `reports.view` | View/download generated reports |
| `reports.export` | Export reports (PDF/Excel/CSV) |

### 2.13 Settings Module

| Permission | Description |
|---|---|
| `settings.view` | View school settings, academic years |
| `settings.update` | Update school settings, create academic years, manage classes/sections/subjects |

### 2.14 Audit Module

| Permission | Description |
|---|---|
| `audit.view` | View audit logs |

### 2.15 Conversations Module

| Permission | Description |
|---|---|
| `messages.send` | Send messages in conversations |
| `messages.view` | View conversations and messages |

---

## 3. Role × Permission Matrix

> ✅ = Granted | ❌ = Not granted | 🔒 = Granted with row-level scope restriction

### 3.1 Students & Users

| Permission | Super Admin | School Admin | Principal | Teacher | Parent | Student | Accountant | Librarian | Transport Admin | Receptionist |
|---|---|---|---|---|---|---|---|---|---|---|
| `students.create` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `students.view` | ✅ | ✅ | ✅ | 🔒 | 🔒 | 🔒 | 🔒 | ❌ | ❌ | ✅ |
| `students.view_sensitive` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `students.update` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `students.delete` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `students.export` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `users.create` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `users.view` | ✅ | ✅ | ✅ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `users.update` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `users.delete` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `users.assign_role` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### 3.2 Attendance

| Permission | Super Admin | School Admin | Principal | Teacher | Parent | Student | Accountant | Librarian | Transport Admin | Receptionist |
|---|---|---|---|---|---|---|---|---|---|---|
| `attendance.create` | ✅ | ✅ | ❌ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `attendance.view` | ✅ | ✅ | ✅ | 🔒 | 🔒 | 🔒 | ❌ | ❌ | ❌ | ❌ |
| `attendance.correct` | ✅ | ✅ | ✅ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `attendance.lock` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `attendance.report` | ✅ | ✅ | ✅ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### 3.3 Timetable & Homework

| Permission | Super Admin | School Admin | Principal | Teacher | Parent | Student | Accountant | Librarian | Transport Admin | Receptionist |
|---|---|---|---|---|---|---|---|---|---|---|
| `timetable.create` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `timetable.view` | ✅ | ✅ | ✅ | ✅ | 🔒 | 🔒 | ❌ | ❌ | ❌ | ❌ |
| `timetable.publish` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `homework.create` | ✅ | ✅ | ❌ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `homework.view` | ✅ | ✅ | ✅ | 🔒 | 🔒 | 🔒 | ❌ | ❌ | ❌ | ❌ |
| `homework.submit` | ❌ | ❌ | ❌ | ❌ | ❌ | 🔒 | ❌ | ❌ | ❌ | ❌ |
| `homework.grade` | ✅ | ✅ | ❌ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### 3.4 Exams & Marks

| Permission | Super Admin | School Admin | Principal | Teacher | Parent | Student | Accountant | Librarian | Transport Admin | Receptionist |
|---|---|---|---|---|---|---|---|---|---|---|
| `exams.create` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `exams.view` | ✅ | ✅ | ✅ | 🔒 | 🔒 | 🔒 | ❌ | ❌ | ❌ | ❌ |
| `exams.enter_marks` | ✅ | ✅ | ❌ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `exams.approve_marks` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `exams.publish` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `exams.report` | ✅ | ✅ | ✅ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### 3.5 Fees

| Permission | Super Admin | School Admin | Principal | Teacher | Parent | Student | Accountant | Librarian | Transport Admin | Receptionist |
|---|---|---|---|---|---|---|---|---|---|---|
| `fees.view` | ✅ | ✅ | ✅ | ❌ | 🔒 | 🔒 | ✅ | ❌ | ❌ | ❌ |
| `fees.create_structure` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `fees.collect` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `fees.pay` | ❌ | ❌ | ❌ | ❌ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ |
| `fees.refund` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `fees.waive` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `fees.report` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |

### 3.6 Library

| Permission | Super Admin | School Admin | Principal | Teacher | Parent | Student | Accountant | Librarian | Transport Admin | Receptionist |
|---|---|---|---|---|---|---|---|---|---|---|
| `library.view` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| `library.manage_books` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `library.issue` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `library.return` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `library.manage_fines` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |

### 3.7 Transport

| Permission | Super Admin | School Admin | Principal | Teacher | Parent | Student | Accountant | Librarian | Transport Admin | Receptionist |
|---|---|---|---|---|---|---|---|---|---|---|
| `transport.view` | ✅ | ✅ | ✅ | ❌ | 🔒 | 🔒 | ❌ | ❌ | ✅ | ❌ |
| `transport.manage` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `transport.assign` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

### 3.8 Communication, Leave, Reports, Settings, Audit

| Permission | Super Admin | School Admin | Principal | Teacher | Parent | Student | Accountant | Librarian | Transport Admin | Receptionist |
|---|---|---|---|---|---|---|---|---|---|---|
| `notifications.view` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `notifications.send` | ✅ | ✅ | ✅ | 🔒 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `notifications.manage_templates` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `leave.create` | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| `leave.view` | ✅ | ✅ | ✅ | 🔒 | ❌ | ❌ | 🔒 | 🔒 | 🔒 | 🔒 |
| `leave.approve` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `messages.send` | ✅ | ✅ | ✅ | ✅ | ✅ | 🔒 | ✅ | ✅ | ✅ | ✅ |
| `messages.view` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `reports.generate` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `reports.view` | ✅ | ✅ | ✅ | 🔒 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `reports.export` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `settings.view` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `settings.update` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `audit.view` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 4. Row-Level Scope Rules

🔒 marks in the matrix above indicate that the permission is granted but **restricted to specific rows**. The service layer enforces these rules.

| Role | Module | Scope Rule | Implementation |
|---|---|---|---|
| **Teacher** | `students.view` | Only students in assigned sections | `WHERE section_id IN (teacher's sections)` |
| **Teacher** | `attendance.create` | Only their assigned sections | Validate `section_id` against `teacher_subjects` |
| **Teacher** | `attendance.view` | Only their assigned sections | Filter by teacher's section assignments |
| **Teacher** | `attendance.correct` | Only their own sessions | `WHERE submitted_by = teacher.user_id` |
| **Teacher** | `attendance.report` | Only their sections | Section-level reports only |
| **Teacher** | `homework.create` | Only their subject+section assignments | Validate against `teacher_subjects` |
| **Teacher** | `homework.view` | Only homework they created | `WHERE teacher_id = teacher.id` |
| **Teacher** | `homework.grade` | Only homework they created | `WHERE teacher_id = teacher.id` |
| **Teacher** | `exams.view` | Only exams involving their subjects | Filter by teacher's subject assignments |
| **Teacher** | `exams.enter_marks` | Only their subject+section | Validate `exam_subject` is their assignment |
| **Teacher** | `exams.report` | Only their sections | Section-level rank lists |
| **Teacher** | `notifications.send` | Only to their sections | Audience filter restricted to section |
| **Teacher** | `users.view` | Only students in their sections | Same as `students.view` scope |
| **Teacher** | `leave.view` | Own leave requests only | `WHERE user_id = teacher.user_id` |
| **Teacher** | `reports.view` | Own section reports | Generated for their sections |
| **Parent** | `students.view` | Only linked children | `WHERE student_id IN (parent's children via student_guardians)` |
| **Parent** | `attendance.view` | Only children's attendance | Join through linked student IDs |
| **Parent** | `homework.view` | Only children's homework | Filter by children's section |
| **Parent** | `exams.view` | Only children's exams/marks | Filter by children's enrollment |
| **Parent** | `fees.view` | Only children's fees | `WHERE student_id IN (parent's children)` |
| **Parent** | `fees.pay` | Only children's fees | Validate student belongs to parent |
| **Parent** | `timetable.view` | Only children's timetable | Filter by children's section |
| **Parent** | `transport.view` | Only children's route/stop | Filter by children's transport assignment |
| **Student** | `students.view` | Own record only | `WHERE student.user_id = current_user.id` |
| **Student** | `attendance.view` | Own attendance only | `WHERE student_id = own student ID` |
| **Student** | `homework.view` | Own section's homework | Filter by enrolled section |
| **Student** | `homework.submit` | Own submissions only | `WHERE student_id = own student ID` |
| **Student** | `exams.view` | Own marks only | `WHERE student_id = own student ID` |
| **Student** | `fees.view` | Own fees only | `WHERE student_id = own student ID` |
| **Student** | `timetable.view` | Own section's timetable | Filter by enrolled section |
| **Student** | `transport.view` | Own route/stop | Filter by own transport assignment |
| **Student** | `messages.send` | To teachers/admin only | Cannot message other students |
| **Accountant** | `students.view` | All school students (fee context) | Name + section for fee matching |
| **Accountant** | `fees.view` | All school fees | Full access within school |
| **Accountant** | `leave.view` | Own leave only | `WHERE user_id = accountant.user_id` |
| **Librarian** | `leave.view` | Own leave only | `WHERE user_id = librarian.user_id` |
| **Transport Admin** | `leave.view` | Own leave only | `WHERE user_id = transport_admin.user_id` |
| **Receptionist** | `leave.view` | Own leave only | `WHERE user_id = receptionist.user_id` |

---

## 5. Role Hierarchy & Escalation Rules

### 5.1 Who Can Assign Roles

| Assigner | Can Assign |
|---|---|
| `super_admin` | All roles including `school_admin` |
| `school_admin` | All roles except `super_admin` and `school_admin` |
| Others | Cannot assign roles |

### 5.2 Escalation Prevention

- No user can assign a role with more permissions than their own
- `super_admin` role assignment requires existing `super_admin` approval
- Role changes are audit-logged with old and new role sets
- A user cannot remove their own last `school_admin` role (prevents lockout)

### 5.3 Multi-Role Resolution

When a user has multiple roles, the effective permission set is the **union** of all role permissions:

```python
effective_permissions = set()
for role in user.roles:
    effective_permissions |= role.permissions
```

Row-level scope uses the **most permissive** scope. Example: if a user is both `teacher` (sees own sections) and `school_admin` (sees all), they see all.

---

## 6. Seed Data

### 6.1 Roles Seed

```sql
INSERT INTO roles (id, name, description, is_system) VALUES
  (gen_random_uuid(), 'super_admin',     'Platform-wide administrator', true),
  (gen_random_uuid(), 'school_admin',    'School-level administrator',  true),
  (gen_random_uuid(), 'principal',       'School principal / director', true),
  (gen_random_uuid(), 'teacher',         'Teaching staff',              true),
  (gen_random_uuid(), 'parent',          'Parent / guardian',           true),
  (gen_random_uuid(), 'student',         'Enrolled student',            true),
  (gen_random_uuid(), 'accountant',      'Finance / accounts staff',    true),
  (gen_random_uuid(), 'librarian',       'Library staff',               true),
  (gen_random_uuid(), 'transport_admin', 'Transport manager',           true),
  (gen_random_uuid(), 'receptionist',    'Front desk / reception',      true);
```

### 6.2 Permissions Seed (60 permissions)

```sql
INSERT INTO permissions (id, name, module, description) VALUES
  -- Students (6)
  (gen_random_uuid(), 'students.create',         'students',  'Create/import students'),
  (gen_random_uuid(), 'students.view',           'students',  'View student data'),
  (gen_random_uuid(), 'students.view_sensitive', 'students',  'View medical/aadhaar data'),
  (gen_random_uuid(), 'students.update',         'students',  'Edit student records'),
  (gen_random_uuid(), 'students.delete',         'students',  'Archive students'),
  (gen_random_uuid(), 'students.export',         'students',  'Export student data'),
  -- Users (5)
  (gen_random_uuid(), 'users.create',       'users',  'Create user accounts'),
  (gen_random_uuid(), 'users.view',         'users',  'View user data'),
  (gen_random_uuid(), 'users.update',       'users',  'Edit user profiles'),
  (gen_random_uuid(), 'users.delete',       'users',  'Deactivate users'),
  (gen_random_uuid(), 'users.assign_role',  'users',  'Manage role assignments'),
  -- Attendance (5)
  (gen_random_uuid(), 'attendance.create',  'attendance', 'Submit attendance'),
  (gen_random_uuid(), 'attendance.view',    'attendance', 'View attendance'),
  (gen_random_uuid(), 'attendance.correct', 'attendance', 'Correct attendance'),
  (gen_random_uuid(), 'attendance.lock',    'attendance', 'Lock attendance sessions'),
  (gen_random_uuid(), 'attendance.report',  'attendance', 'Generate attendance reports'),
  -- Timetable (3)
  (gen_random_uuid(), 'timetable.create',  'timetable', 'Create timetables'),
  (gen_random_uuid(), 'timetable.view',    'timetable', 'View timetables'),
  (gen_random_uuid(), 'timetable.publish', 'timetable', 'Publish timetables'),
  -- Homework (4)
  (gen_random_uuid(), 'homework.create', 'homework', 'Create homework'),
  (gen_random_uuid(), 'homework.view',   'homework', 'View homework'),
  (gen_random_uuid(), 'homework.submit', 'homework', 'Submit homework'),
  (gen_random_uuid(), 'homework.grade',  'homework', 'Grade homework'),
  -- Exams (6)
  (gen_random_uuid(), 'exams.create',        'exams', 'Create exams'),
  (gen_random_uuid(), 'exams.view',          'exams', 'View exams'),
  (gen_random_uuid(), 'exams.enter_marks',   'exams', 'Enter marks'),
  (gen_random_uuid(), 'exams.approve_marks', 'exams', 'Approve marks'),
  (gen_random_uuid(), 'exams.publish',       'exams', 'Publish results'),
  (gen_random_uuid(), 'exams.report',        'exams', 'Exam reports'),
  -- Fees (7)
  (gen_random_uuid(), 'fees.view',             'fees', 'View fee data'),
  (gen_random_uuid(), 'fees.create_structure', 'fees', 'Manage fee structures'),
  (gen_random_uuid(), 'fees.collect',          'fees', 'Collect payments'),
  (gen_random_uuid(), 'fees.pay',              'fees', 'Make online payments'),
  (gen_random_uuid(), 'fees.refund',           'fees', 'Process refunds'),
  (gen_random_uuid(), 'fees.waive',            'fees', 'Apply waivers/discounts'),
  (gen_random_uuid(), 'fees.report',           'fees', 'Financial reports'),
  -- Library (5)
  (gen_random_uuid(), 'library.view',         'library', 'View books'),
  (gen_random_uuid(), 'library.manage_books', 'library', 'Manage catalog'),
  (gen_random_uuid(), 'library.issue',        'library', 'Issue books'),
  (gen_random_uuid(), 'library.return',       'library', 'Return books'),
  (gen_random_uuid(), 'library.manage_fines', 'library', 'Manage fines'),
  -- Transport (3)
  (gen_random_uuid(), 'transport.view',   'transport', 'View transport'),
  (gen_random_uuid(), 'transport.manage', 'transport', 'Manage routes/buses'),
  (gen_random_uuid(), 'transport.assign', 'transport', 'Assign students'),
  -- Notifications (3)
  (gen_random_uuid(), 'notifications.view',             'notifications', 'View notifications'),
  (gen_random_uuid(), 'notifications.send',             'notifications', 'Send notifications'),
  (gen_random_uuid(), 'notifications.manage_templates', 'notifications', 'Manage templates'),
  -- Leave (3)
  (gen_random_uuid(), 'leave.create',  'leave', 'Submit leave'),
  (gen_random_uuid(), 'leave.view',    'leave', 'View leave requests'),
  (gen_random_uuid(), 'leave.approve', 'leave', 'Approve/reject leave'),
  -- Reports (3)
  (gen_random_uuid(), 'reports.generate', 'reports', 'Generate reports'),
  (gen_random_uuid(), 'reports.view',     'reports', 'View reports'),
  (gen_random_uuid(), 'reports.export',   'reports', 'Export reports'),
  -- Settings (2)
  (gen_random_uuid(), 'settings.view',   'settings', 'View settings'),
  (gen_random_uuid(), 'settings.update', 'settings', 'Update settings'),
  -- Messages (2)
  (gen_random_uuid(), 'messages.send', 'messages', 'Send messages'),
  (gen_random_uuid(), 'messages.view', 'messages', 'View messages'),
  -- Audit (1)
  (gen_random_uuid(), 'audit.view', 'audit', 'View audit logs');
```

### 6.3 Role-Permission Mapping

The `role_permissions` table is seeded based on the matrix in Section 3. The mapping is generated by a migration script that cross-references role slugs with permission names.

```python
# Seed script pattern (in Alembic migration)
ROLE_PERMISSIONS = {
    "super_admin": ["*"],  # All permissions
    "school_admin": [
        "students.*", "users.*", "attendance.*", "timetable.*",
        "homework.create", "homework.view", "homework.grade",
        "exams.*", "fees.view", "fees.create_structure", "fees.collect",
        "fees.refund", "fees.waive", "fees.report",
        "library.view", "library.manage_books", "library.issue",
        "library.return", "library.manage_fines",
        "transport.*", "notifications.*",
        "leave.create", "leave.view", "leave.approve",
        "messages.*", "reports.*", "settings.*", "audit.view",
    ],
    "principal": [
        "students.view", "students.view_sensitive", "students.export",
        "users.view",
        "attendance.view", "attendance.correct", "attendance.lock", "attendance.report",
        "timetable.view",
        "homework.view", "exams.view", "exams.approve_marks", "exams.publish", "exams.report",
        "fees.view", "fees.report",
        "library.view", "transport.view",
        "notifications.view", "notifications.send",
        "leave.create", "leave.view", "leave.approve",
        "messages.*", "reports.*", "settings.view", "audit.view",
    ],
    "teacher": [
        "students.view",
        "attendance.create", "attendance.view", "attendance.correct", "attendance.report",
        "timetable.view",
        "homework.create", "homework.view", "homework.grade",
        "exams.view", "exams.enter_marks",
        "library.view",
        "notifications.view", "notifications.send",
        "leave.create", "leave.view",
        "messages.*", "reports.view",
    ],
    "parent": [
        "students.view",
        "attendance.view",
        "timetable.view",
        "homework.view",
        "exams.view",
        "fees.view", "fees.pay",
        "transport.view",
        "notifications.view",
        "messages.*",
    ],
    "student": [
        "students.view",
        "attendance.view",
        "timetable.view",
        "homework.view", "homework.submit",
        "exams.view",
        "fees.view",
        "library.view",
        "transport.view",
        "notifications.view",
        "messages.*",
    ],
    "accountant": [
        "students.view",
        "fees.*",
        "notifications.view",
        "leave.create", "leave.view",
        "messages.*", "reports.*",
    ],
    "librarian": [
        "library.*",
        "notifications.view",
        "leave.create", "leave.view",
        "messages.*",
    ],
    "transport_admin": [
        "transport.*",
        "notifications.view",
        "leave.create", "leave.view",
        "messages.*",
    ],
    "receptionist": [
        "students.create", "students.view", "students.update",
        "notifications.view",
        "leave.create", "leave.view",
        "messages.*",
    ],
}
```

---

## 7. Assumptions and Open Questions

### Assumptions

1. `super_admin` has all permissions implicitly; checked with `is_super_admin` flag, not by iterating permissions.
2. Custom roles (school-defined) deferred to Phase 5+. Phase 1–4 uses only the 10 system roles.
3. Row-level scope is enforced in the service/repository layer, not via additional DB RLS policies (performance and clarity).
4. Permission names in the JWT token are the flattened union of all role permissions — keeps authorization checks simple (single `in` check).
5. The `principal` role is distinct from `school_admin` — principals have read-heavy access with approval powers but cannot modify settings or manage users.
6. `receptionist` is intentionally limited — handles student intake paperwork but not academic or financial data.

### Open Questions

1. **Department-level scope:** Should principals/vice-principals be scoped to specific departments (e.g., primary vs. secondary), or always school-wide?
2. **Delegation:** Should a teacher be able to delegate attendance submission to another teacher for their section (e.g., substitute teacher), and how does that affect scope rules?
3. **Parent-teacher messaging:** Should parents be allowed to initiate conversations with any teacher, or only their child's assigned teachers?
4. **Student messaging:** Should students be able to message only teachers, or also school admin and other roles?
5. **Custom permissions per school:** When custom roles arrive in Phase 5, should schools be able to create entirely new permissions, or only re-combine existing system permissions into new roles?
