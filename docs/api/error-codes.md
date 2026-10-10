# Error Codes Catalog

| Code | HTTP Status | Meaning | User-facing handling |
|---|---|---|---|
| VALIDATION_ERROR | 422 | Input validation failed | Show inline field errors |
| UNAUTHORIZED | 401 | Missing or invalid token | Redirect to login |
| FORBIDDEN | 403 | Missing permissions | Show access denied screen |
| NOT_FOUND | 404 | Resource does not exist | Show 404 page |
| CONFLICT | 409 | Resource already exists | Show conflict error |
| RATE_LIMITED | 429 | Too many requests | Show retry-after message |
| INTERNAL_ERROR | 500 | Server crash | Show generic error with request_id |
