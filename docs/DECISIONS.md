# Architecture Decision Records (ADR)

> Living document. New decisions appended at the bottom. Never delete entries.

---

## ADR-001: Modular Monolith over Microservices

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** Need to choose between microservices (separate deployable per module) and a modular monolith (single deployable with strict internal boundaries).  
**Options:**
1. Microservices — independent scaling, language flexibility, team isolation
2. Modular monolith — simpler ops, shared DB transactions, lower latency, easier debugging

**Decision:** Modular monolith. At our scale (1–100 schools), the operational overhead of microservices (service mesh, distributed tracing, eventual consistency) is not justified. Modules communicate through service interfaces and domain events within the same process.  
**Consequences:** Must enforce module boundaries at code review level. If we reach 500+ schools and need independent scaling, we can extract modules into services along existing interfaces.

---

## ADR-002: Celery over ARQ/RQ for Background Jobs

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** Need a background job framework for: PDF generation, notification fan-out, bulk imports, payment reconciliation, scheduled tasks.  
**Options:**
1. Celery — mature, beat scheduler, retries, rate limits, monitoring (Flower), large ecosystem
2. ARQ — lightweight, async-native, simpler
3. RQ — simple, Redis-only, minimal features

**Decision:** Celery. The scheduling (Beat), retry policies, queue routing, and monitoring tooling are essential for our workload. ARQ lacks scheduling and has weaker tooling. RQ lacks scheduling and priority routing.  
**Consequences:** Celery adds complexity (worker processes, beat scheduler). Mitigated by Docker Compose managing all processes.

---

## ADR-003: Argon2id over bcrypt for Password Hashing

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** Need a password hashing algorithm that resists GPU/ASIC attacks.  
**Options:**
1. bcrypt — battle-tested, widely used, 72-byte password limit
2. Argon2id — memory-hard, OWASP recommended, no password length limit

**Decision:** Argon2id. OWASP's current recommendation. Memory-hardness provides better resistance to parallel attacks than bcrypt's CPU-only hardness.  
**Consequences:** Slightly less library maturity than bcrypt, but `argon2-cffi` is well-maintained. If migrating from bcrypt, rehash on login.

---

## ADR-004: RS256 over HS256 for JWT Signing

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** Choose JWT signing algorithm for access tokens.  
**Options:**
1. HS256 — symmetric, simpler, both sides need the secret
2. RS256 — asymmetric, only backend has private key, any service can verify with public key

**Decision:** RS256. Allows Next.js admin and future services to verify tokens without access to the signing key. Better security posture.  
**Consequences:** Key pair management (rotation every 90 days). Slightly larger tokens. JWKS endpoint needed.

---

## ADR-005: NUMERIC(12,2) over Integer Paise for Money

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** Original design used integer paise. Master context specifies `NUMERIC(12,2)`.  
**Options:**
1. Integer paise (e.g., 500000 = ₹5,000.00) — no rounding errors, simpler arithmetic
2. NUMERIC(12,2) — human-readable in DB, standard SQL money handling

**Decision:** `NUMERIC(12,2)` per Master Context §4. Server-side calculation only. Never float.  
**Consequences:** Must ensure all money calculations use NUMERIC/Decimal in Python, never float. Display formatting is client responsibility. Database design docs updated to reflect this.

---

## ADR-006: Single Shared Schema over Schema-per-Tenant

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** Multi-tenancy strategy for 1–100+ schools.  
**Options:**
1. Schema-per-tenant — strong isolation, complex migrations
2. DB-per-tenant — strongest isolation, highest ops overhead
3. Shared schema with `school_id` — simplest, cross-tenant queries possible, needs RLS

**Decision:** Shared schema with `school_id`. Three-layer enforcement: JWT claim → repository WHERE → PostgreSQL RLS.  
**Consequences:** Must be vigilant about tenant isolation. Every query, every test must verify. RLS as safety net catches bugs.

---

## ADR-007: Pre-Signed URLs over Multipart Upload for Files

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** How should clients upload files?  
**Options:**
1. Multipart to API server — simple client code, API handles storage, bottleneck at API
2. Pre-signed URLs (client → S3 direct) — API generates URL, client uploads directly

**Decision:** Pre-signed URLs. Offloads bandwidth from API servers. Enables horizontal API scaling without file buffering. Client gets PUT URL, uploads directly to S3/MinIO.  
**Consequences:** More complex client logic (two-step: get URL, upload). Upload confirmation step needed. Content-Type validation at both URL generation and confirmation.

---

## ADR-008: Offset + Cursor Pagination Strategy

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** Need pagination for all list endpoints.  
**Options:**
1. Offset only — simple, allows jumping to page N, degrades on large offsets
2. Cursor only — performant at any depth, no page jumping
3. Both — offset for admin tables (need page N), cursor for feeds/sync

**Decision:** Both. Offset for admin tables (students, fees, staff). Cursor for high-volume append-only data (messages, notifications, audit logs). Max page size: 100.  
**Consequences:** Two pagination implementations to maintain. Client must handle both patterns.

---

## ADR-009: structlog over stdlib logging

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** Need structured, machine-parseable logs with request context.  
**Options:**
1. Python stdlib `logging` — built-in, but unstructured by default
2. `structlog` — structured JSON, context variables, processor chain

**Decision:** structlog with JSON output. Every log line includes `request_id`, `user_id`, `school_id`. Sensitive field redaction via processor.  
**Consequences:** Additional dependency. Team must use structlog API (`log.info("msg", key=val)`) not print/stdlib.

---

## ADR-010: Tailwind CSS for Admin Web

**Date:** 2025-10-04  
**Status:** Accepted  
**Context:** Master Context specifies Tailwind CSS for the Next.js admin.  
**Decision:** Tailwind CSS per locked tech stack. Utility-first, consistent with Next.js ecosystem.  
**Consequences:** All admin UI styling uses Tailwind utilities. Custom CSS only for truly custom components.

---

## ADR-011: Rollup over Live Aggregation for Analytics
**Date:** 2026-10-05  
**Status:** Accepted  
**Context:** Dashboards require fast load times for aggregate metrics.  
**Decision:** Use denormalized rollup tables (e.g., `analytics_attendance_daily`) built asynchronously via Celery jobs instead of querying live transactional tables.  
**Consequences:** Data on dashboards is eventually consistent (as of the last rollup run). Live tables are protected from analytical queries.

---

## ADR-012: Widget Isolation on Dashboards
**Date:** 2026-10-05  
**Status:** Accepted  
**Context:** Dashboards compose multiple widgets. A single failing widget should not break the entire page.  
**Decision:** Widget Framework returns a standardized `WidgetResult` with a `status` (ok, empty, error). The frontend renders per-widget error states.  
**Consequences:** Each widget must handle its own exceptions. The frontend needs robust fallback components.

---

## ADR-013: Finance Excluded from Risk Scoring
**Date:** 2026-10-05  
**Status:** Accepted  
**Context:** We need a transparent student risk score for interventions.  
**Decision:** Risk scoring uses pure rules based on attendance, behavior, and academics. Financial data (unpaid fees) is strictly excluded to prevent bias or penalty for socioeconomic status.  
**Consequences:** Unpaid fees must be handled exclusively by the finance module. Risk scores reflect only student engagement and academic health.

---

## ADR-014: Append-Only Consent Model for Minors
**Date:** 2026-10-05  
**Status:** Accepted  
**Context:** Privacy regulations require clear consent tracking, especially for minors.  
**Decision:** Consents are stored in an append-only table. Withdrawing consent sets a `withdrawn_at` timestamp on the old record and leaves it intact.  
**Consequences:** Complete audit trail of consent history. Queries must explicitly filter for `withdrawn_at IS NULL`.

---

## ADR-015: Anonymize over Delete for Erasure
**Date:** 2026-10-05  
**Status:** Accepted  
**Context:** Data erasure requests must balance privacy with referential integrity (e.g., keeping aggregate attendance numbers accurate).  
**Decision:** Erasure requests trigger an anonymization process that scrambles PII but retains the primary keys and non-identifying aggregate data, rather than hard-deleting rows.  
**Consequences:** Custom anonymization scripts must be maintained. Hard deletes are reserved for GDPR-style total wipe requests only when legally required.

---

## ADR-016: Two-Person Approval for Erasure
**Date:** 2026-10-05  
**Status:** Accepted  
**Context:** Data erasure is destructive and irreversible.  
**Decision:** Erasure requests require approval from a second authorized user (the approver cannot be the requester).  
**Consequences:** Erasing data is a multi-step process. UI must handle the "waiting for approval" state.

---

## ADR-017: AI Output Isolation and Approval (Human-in-the-Loop)
**Date:** 2026-10-05  
**Status:** Accepted  
**Context:** AI-generated content (like student progress notes) carries hallucination and bias risks.  
**Decision:** AI output is always saved as a "draft". It requires explicit human approval before being visible to parents or becoming part of the official record.  
**Consequences:** Extra workflow steps for teachers/admins. Reduces risk of inappropriate AI content reaching end-users.

---

## ADR-018: Provider Abstraction and Pseudonymization for AI
**Date:** 2026-10-05  
**Status:** Accepted  
**Context:** We need to use LLMs (e.g., Anthropic Claude) without leaking PII or locking into one vendor.  
**Decision:** Abstract the LLM provider behind an interface. Before sending context to the LLM, pass it through a Redactor to strip PII (names, emails, phones).  
**Consequences:** The application uses internal IDs in prompts. The prompt registry manages templates. Redaction logic requires maintenance and testing.
