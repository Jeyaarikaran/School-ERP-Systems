# Phase 9 API Handoff: Library and Transport

## Endpoint Overview

### Library
| Use Case | Method | Path | Auth / Permission | Pagination |
|----------|--------|------|-------------------|------------|
| Search Catalog | GET | `/library/books` | Bearer (`library.view`) | Cursor / Offset |
| Add Book | POST | `/library/books` | Bearer (`library.manage_books`) | None |
| Add Copies | POST | `/library/books/{id}/copies` | Bearer (`library.manage_books`) | None (bulk) |
| Issue Book | POST | `/library/circulation/issue` | Bearer (`library.circulate`) | None |
| Return Book | POST | `/library/circulation/return` | Bearer (`library.circulate`) | None |
| Renew Book | POST | `/library/circulation/renew` | Bearer (`library.circulate`) | None |
| Member Dashboard | GET | `/library/members/{id}/status`| Bearer (`library.circulate` or `library.view_own`) | None |
| Member History | GET | `/library/members/{id}/history`| Bearer (`library.circulate` or `library.view_own`) | Cursor |
| List Fines | GET | `/library/fines` | Bearer (`library.fines_manage`) | Offset |
| Waive Fine | POST | `/library/fines/{id}/waive` | Bearer (`library.fines_waive`) | None |
| Stocktake Scans | POST | `/library/stocktakes/{id}/scans`| Bearer (`library.stocktake`) | None (bulk, idempotent) |

### Transport
| Use Case | Method | Path | Auth / Permission | Pagination |
|----------|--------|------|-------------------|------------|
| List Buses | GET | `/transport/buses` | Bearer (`transport.view`) | Offset |
| List Routes | GET | `/transport/routes` | Bearer (`transport.view`) | Offset |
| Assign Bus | POST | `/transport/route-assignments`| Bearer (`transport.manage_assets`) | None |
| Enroll Student | POST | `/transport/enrollments` | Bearer (`transport.assign_students`) | None |
| List Trip Runs | GET | `/transport/trip-runs` | Bearer (`transport.view`) | Cursor / Offset |
| Driver Today | GET | `/transport/trip-runs/mine/today`| Bearer (`transport.run_trips`) | None |
| Boarding Batch | POST | `/transport/trip-runs/{id}/events`| Bearer (`transport.run_trips`) | None (bulk, idempotent) |
| Parent View | GET | `/transport/me?student_id=` | Bearer (`transport.view_own`) | None |

## Request / Response Examples

### Issue Book
**POST** `/library/circulation/issue`
**Headers:** `Idempotency-Key: req_123`
```json
{
  "member_barcode": "STU-00123",
  "copy_barcode": "LIB-00456"
}
```
**Response (200 OK):**
```json
{
  "id": "uuid",
  "due_date": "2023-11-15",
  "status": "issued"
}
```

### Boarding Event Batch
**POST** `/transport/trip-runs/{id}/events`
**Headers:** `Idempotency-Key: req_456`
```json
{
  "events": [
    {
      "client_event_id": "evt_abc123",
      "student_id": "uuid",
      "event_type": "boarded",
      "occurred_at": "2023-11-01T08:05:00Z"
    }
  ]
}
```
**Response (200 OK):**
```json
{
  "processed": 1,
  "warnings": []
}
```

## Error Codes
- `LIMIT_REACHED`: Member cannot borrow more books. Present UI to override if role permits.
- `UNPAID_FINES_BLOCK`: Unpaid fine threshold crossed. Direct user to fee settlement.
- `COPY_NOT_AVAILABLE`: Copy is lost, damaged, or already issued.
- `ROUTE_FULL`: Selected transport route exceeds bus capacity. Show alternative routes provided in error details.
- `COMPLIANCE_EXPIRED`: Bus/driver document expired. Block action; present override if role permits.

## Idempotency Rules
All POST endpoints related to circulation (`/issue`, `/return`, `/renew`) and transport boarding (`/events`) require the `Idempotency-Key` header. Double scans from barcode readers or offline mobile retries will yield the original `200 OK` response without side-effects.

## Visibility & Masking
- **Driver License:** `license_number_enc` is masked (e.g. `********1234`) unless the user possesses `transport.view_sensitive`.
- **Parent View:** `/transport/me` excludes driver phone numbers unless `transport.show_driver_contact` is true in system settings.
