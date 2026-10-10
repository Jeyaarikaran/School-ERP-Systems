# Frontend Contract Gaps

| Endpoint | Expected | Actual | Proposed Fix | Workaround Used |
|---|---|---|---|---|
| OpenAPI export | `docs/api/openapi.json` exists | Missing from repository | Backend should implement `scripts/export_openapi.py` | Manually created a stub `openapi.json` for `/health` and `/ready` to unblock client generation. |
| Error Codes | `docs/api/error-codes.md` exists | Missing from repository | Backend should auto-generate | Manually created catalog with generic 400/500 codes. |
