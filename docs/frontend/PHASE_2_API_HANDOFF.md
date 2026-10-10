# PHASE 2 API HANDOFF: Auth, RBAC & Multi-Tenancy

## 1. Overview
This document outlines the frontend integration contract for Phase 2, covering Authentication, Session Management, Roles, and Tenancy endpoints.

## 2. Endpoints

| Screen/Use-case | Method | Path | Caller Role | Permission | Paginated | Idempotent |
|---|---|---|---|---|---|---|
| Login | POST | `/api/v1/auth/login` | Any (unauth) | none | No | No |
| 2FA Login | POST | `/api/v1/auth/login/2fa` | Any (with token) | none | No | No |
| Refresh | POST | `/api/v1/auth/refresh` | Any | none | No | No |
| Logout | POST | `/api/v1/auth/logout` | Any | none | No | No |
| Logout All | POST | `/api/v1/auth/logout-all` | Any | none | No | No |
| Password Forgot | POST | `/api/v1/auth/password/forgot` | Any | none | No | No |
| Password Reset | POST | `/api/v1/auth/password/reset` | Any (with token) | none | No | No |
| Password Change | POST | `/api/v1/auth/password/change` | Any | none | No | No |
| My Profile | GET | `/api/v1/auth/me` | Any | none | No | No |
| View Users | GET | `/api/v1/users` | Admin | `users.view` | Yes (offset) | No |
| Create User | POST | `/api/v1/users` | Admin | `users.create` | No | Yes (header required) |
| Manage Roles | POST | `/api/v1/roles` | Admin | `roles.manage` | No | No |
| View Audit Logs | GET | `/api/v1/audit-logs` | Admin | `audit.view` | Yes (offset) | No |
| Create School | POST | `/api/v1/platform/schools` | Super Admin | none | No | Yes (header required) |

## 3. Behavior Rules for UI

### 3.1 Login & Tenancy
- **Tenant users** must provide `school_code`, `identifier` (email or phone), and `password`. Platform users omit `school_code`.
- **2FA Challenge:** If a user has 2FA mandated (e.g. School Admin), a `200 OK` from `/login` may yield `{ "data": { "requires_2fa": true, "challenge_token": "..." } }`. The UI must then call `/auth/login/2fa` with the TOTP or recovery code.
- Tokens should be stored securely. Access tokens are valid for 15 minutes. Refresh tokens rotate on every use.

### 3.2 Security & Sessions
- **Web Admin:** Does NOT handle JWTs in JavaScript. It proxies through Next.js BFF which stores httpOnly cookies.
- **Mobile:** Stores tokens in `flutter_secure_storage`.
- **Refresh Concurrency (Mobile):** If 3 requests fail with 401 simultaneously, the app must queue them, perform exactly **one** refresh call, and replay the 3 requests with the new token. Re-using a rotated refresh token deliberately revokes all sessions.
- **Account Enumeration:** The backend intentionally returns the same generic message for "Unknown User", "Wrong Password", and "Forgot Password" to prevent enumeration.

### 3.3 Permissions & Routing
- `GET /auth/me` returns `roles` and `effective_permissions`. The UI should use this array to dynamically hide routes (e.g. hide "Users" tab if `users.view` is absent). However, the backend strictly enforces permissions.

### 3.4 Audit Log Viewer
- Exposes `old_value` and `new_value` JSON blobs. The UI should display these safely, ideally escaping HTML and presenting them in a collapsed JSON-tree view.

## 4. Error Codes (Added in Phase 2)
| Code | HTTP Status | Meaning | Recommended UX |
|---|---|---|---|
| `INVALID_CREDENTIALS` | 401 | Wrong password or user | "Invalid credentials provided." |
| `ACCOUNT_LOCKED` | 429 | Lockout after max attempts | "Account locked due to too many failures. Try again in 15 mins." |
| `REQUIRES_2FA` | 401 | 2FA setup or challenge required | Show 2FA screen |
| `IDEMPOTENCY_KEY_REUSED` | 422 | Payload changed for existing key | "Invalid retry logic." (Developer error) |
| `REQUEST_IN_PROGRESS` | 409 | Idempotent key already executing | "Please wait, request is processing." |
| `CANNOT_REMOVE_LAST_ADMIN`| 403 | Escalation guard tripped | "Cannot remove the last active School Admin." |

## 5. Examples

**Success Response Envelope:**
```json
{
  "success": true,
  "message": "LOGIN_SUCCESS",
  "data": {
    "access_token": "ey...",
    "refresh_token": "rand..."
  },
  "meta": {
    "request_id": "uuid-1234"
  }
}
```
