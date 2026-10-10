# Load Test & Capacity Plan

## 1. Load Test Setup
- **Tool:** k6
- **Script:** `backend/tests/load/load_test.js`
- **Scenarios:**
  - Ramp-up: 50 CCU (30s)
  - Steady State: 100 CCU (1m)
  - Spike/Burst: 500 CCU (30s)

## 2. Simulated Results
> *Note: These are baseline targets as real infrastructure is not provisioned.*
- **Target p95 Latency:** < 500ms
- **Target Error Rate:** < 1%
- **Bottleneck Identifications:**
  - **Database Connections:** PgBouncer required for connection pooling > 100 CCU.
  - **Rollup Queries:** Complex dashboard aggregations are slow. Mitigated by `RollupService` async processing.
  
## 3. Capacity Plan
To support **500 Concurrent Users** (representing approx. 50-100 active schools with parents checking results simultaneously):
- **API Nodes:** 4x instances (2 vCPU, 4GB RAM) running `uvicorn` with 4 workers each.
- **Database:** PostgreSQL 16 (4 vCPU, 16GB RAM) + PgBouncer (pool size: 200).
- **Redis:** Memory-optimized instance (2GB RAM) for rate-limiting, Celery brokering, and caching.
- **Background Workers:** 2x instances running Celery workers for imports, emails, and rollups.

> **Status:** Partially Verified. K6 script created. Real stress testing requires the staging environment.
