# Backend Security Checklist (ASVS & Infrastructure)

## Application Security (FastAPI)
- [x] **Rate Limiting**: Configured `RateLimitMiddleware` (600 req/min) using Redis.
- [x] **Security Headers**: HSTS, X-Content-Type-Options, X-Frame-Options configured via `SecurityHeadersMiddleware`.
- [x] **Secret Management**: JWT Keys, DB Passwords, and API Keys injected via environment variables (pydantic-settings).
- [x] **CORS Strict**: Allowed origins restricted to environment settings (`settings.cors_origins`).
- [x] **Error Traces**: Stack traces hidden in production. Error IDs returned in 500s.

## Infrastructure & Data Security
- [ ] **Database Encryption**: Cloud SQL configured for CMEK (Customer Managed Encryption Keys). *(Requires cloud provider config)*
- [x] **RLS Enforcement**: Every table inherits `TenantMixin`. Verified no cross-tenant leakage.
- [x] **PII Redaction**: Sentry `beforeSend` or structlog processors scrub PII (emails, phone numbers, auth tokens).
- [ ] **WAF Configuration**: Cloudflare/AWS WAF blocking OWASP top 10. *(Requires cloud infrastructure)*
- [x] **Dependency Scanning**: `npm audit` and `pip-audit` / Trivy scans configured in CI.

> **Status:** All application-level controls are Verified. Infrastructure-level controls require cloud environment deployment (Not Verifiable Here).
