# PHASE 3 API HANDOFF: People and Academic Structure

## 1. Overview
This document specifies the integration contract for Academic Years, Classes, Sections, Subjects, Students, Guardians, Staff, File Uploads, Bulk Imports, and Global Search.

## 2. Endpoints

| Screen/Use-case | Method | Path | Caller Role | Permission | Paginated | Idempotent |
|---|---|---|---|---|---|---|
| Academic Years | GET | `/api/v1/academic-years` | Admin | `academic_years.view` | Yes | No |
| Classes | GET | `/api/v1/classes` | Admin | `classes.view` | Yes | No |
| Sections | GET | `/api/v1/sections` | Admin | `sections.view` | Yes | No |
| Roster Delta Sync | GET | `/api/v1/sync/rosters` | Any | none | Yes (cursor) | No |
| Search | GET | `/api/v1/search` | Any | none | No (limit 10) | No |
| View Students | GET | `/api/v1/students` | Admin/Teacher | `students.view` | Yes (limit 100) | No |
| Admit Student | POST | `/api/v1/students` | Admin | `students.create` | No | Yes |
| Student Detail | GET | `/api/v1/students/{id}` | Admin/Teacher/Parent/Self | `students.view` | No | No |
| View Guardians | GET | `/api/v1/guardians` | Admin | `guardians.view` | Yes | No |
| My Children | GET | `/api/v1/me/children` | Parent | none | No | No |
| View Staff | GET | `/api/v1/staff` | Admin | `staff.view` | Yes | No |
| Upload Photo | POST | `/api/v1/students/{id}/photo` | Admin | `documents.manage` | No | No |
| Download Document | GET | `/api/v1/files/{id}/url` | Auth | none (scope checked) | No | No |
| Import Bulk | POST | `/api/v1/imports` | Admin | `imports.run` | No | Yes |
| Promotion Preview | POST | `/api/v1/promotions/preview` | Admin | `enrollments.promote` | No | No |
| Promotion Execute | POST | `/api/v1/promotions/execute` | Admin | `enrollments.promote` | No | Yes |

## 3. Behavior Rules for UI

### 3.1 Field Tiers (Basic, Standard, Sensitive)
- Response schemas dynamically remove fields based on the caller's permission (`students.view_sensitive`).
- Missing fields are ABSENT from the JSON (not `null`). Do not rely on undefined fields. Do not render placeholders like "Not Provided" if the field simply wasn't sent.

### 3.2 Row Scope (404 Not Found)
- The server enforces scope. If a Teacher tries to fetch a student outside their assigned sections, the backend returns 404 to prevent enumeration. Do not assume the student was deleted; they are just out of scope.

### 3.3 Admissions & Guardian Linking
- **Guardian matching:** If a newly entered guardian phone number matches an existing guardian, the backend will return a conflict or matching state. The UI MUST prompt the admin to confirm linking to the existing guardian rather than creating a duplicate person.
- Server generates the admission number using its own sequence; do not generate it on the client.

### 3.4 Uploads & Signed URLs
- Photos: max 2MB (JPEG/PNG/WebP).
- Documents: max 10MB (PDF/JPEG/PNG).
- All files are subject to malware scanning. They may enter `pending_scan` status. Downloads are blocked until clean.
- To download, call `GET /files/{id}/url` which returns a short-lived (5 min) signed URL. Fetch this URL just-in-time when the user clicks; do not cache it.

### 3.5 Bulk Import Flow
- Uses a wizard flow. 
- Upload -> receive `job_id`. 
- Poll the job. If validation fails, download the errors CSV. 
- The default behavior is all-or-nothing (if 1 row fails, the entire batch fails). Provide an explicit "Import valid rows only" checkbox in the UI.

### 3.6 Promotion Flow
- Two steps. (1) `/preview` returns the proposed transitions for the entire batch. (2) `/execute` performs the actual rollover asynchronously. 

### 3.7 Roster Delta Sync (Offline Support)
- Loop `GET /sync/rosters?cursor={cursor}` until `has_more=false`.
- Persist the changes (upserts and tombstones) to a local cache (e.g. SQLite/Drift).
- Always save the latest `cursor` returned by the backend.

## 4. Error Codes (Added in Phase 3)
| Code | HTTP Status | Meaning | Recommended UX |
|---|---|---|---|
| `GUARDIAN_PHONE_CONFLICT` | 409 | Phone already exists | "This phone number belongs to existing guardian X. Link them?" |
| `FILE_TOO_LARGE` | 413 | Upload exceeds limits | "File must be smaller than 10MB." |
| `INVALID_FILE_TYPE` | 415 | Extension or MIME rejected | "Please upload PDF, PNG, or JPEG." |
| `FILE_PENDING_SCAN` | 403 | Antivirus scanning in progress | "This file is still being scanned for malware." |
| `OUT_OF_SCOPE` | 404 | User lacks row access | (Handle transparently like a real 404) |
