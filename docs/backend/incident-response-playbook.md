# Incident Response Playbook

## 1. Incident Roles
- **Incident Commander (IC):** Coordinates the response, makes decisions, manages communication.
- **Technical Lead:** Investigates root cause, implements fixes.
- **Communications Lead:** Drafts and sends updates to affected schools/parents.

## 2. Severity Levels
- **SEV-1 (Critical):** System down for all schools, widespread data corruption, or active security breach. RTO: < 1 hr.
- **SEV-2 (High):** Major feature broken (e.g., attendance sync failing, payments failing) for multiple schools. RTO: < 4 hrs.
- **SEV-3 (Medium):** Non-critical feature broken or degraded performance. RTO: < 24 hrs.

## 3. Playbook: Security Breach (Data Leak / Unauthorized Access)
1. **Identify & Contain:** Immediately revoke compromised credentials (DB passwords, API keys). Block suspicious IPs via WAF. Put system in Maintenance Mode if data exfiltration is ongoing.
2. **Investigate:** Analyze access logs (CloudWatch/access_log) and Audit logs to determine the scope of the breach (which tenants were accessed).
3. **Eradicate:** Patch the vulnerability, deploy fix, rotate all affected secrets (including JWT keys forcing global logout).
4. **Communicate:** Notify affected schools within 72 hours per DPDP Act guidelines. Provide details on what data was exposed.
5. **Recover:** Lift Maintenance Mode and monitor closely for 48 hours.

## 4. Playbook: Database Performance Degradation
1. **Identify:** Alerts fire for high CPU/Memory on RDS, or p95 API latency > 2000ms.
2. **Investigate:** Check `pg_stat_activity` for long-running queries or lock contention. Check PgBouncer connection saturation.
3. **Mitigate:** Kill runaway queries. If index is missing, add `CONCURRENTLY`. If scale is the issue, trigger an urgent vertical scale (requires brief downtime).
4. **Recover:** Verify API latency returns to baseline.

## 5. Post-Incident Review (Blameless)
Within 48 hours of any SEV-1 or SEV-2 incident, a document must be written detailing:
- Timeline of events
- Root cause (5 Whys)
- Action items to prevent recurrence.
