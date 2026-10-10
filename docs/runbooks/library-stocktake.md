# Runbook: Library Stocktake

**Context:** The library performs a periodic physical inventory (stocktake) to locate missing copies and verify shelf placement.

## 1. Initiation
1. Librarian opens a new Stocktake via `POST /library/stocktakes`.
2. Define `scope_type` (e.g., `all`, `category`, or `shelf`).

## 2. Scanning Phase
1. Staff use barcode scanners (or mobile devices) to scan every physical book.
2. Scans are sent via `POST /library/stocktakes/{id}/scans`. 
   - *Note:* This endpoint is highly optimized and idempotent. It does not perform heavy validation synchronously.

## 3. Review and Closure
1. Librarian generates the discrepancy report: `GET /library/stocktakes/{id}/report`.
   - **Expected but not scanned:** Books the system thinks are on the shelf, but were missed. (Candidates to be marked `missing`).
   - **Scanned but unexpected:** Books physically present but marked as `issued` or `lost` in the system.
2. Resolve discrepancies manually (e.g., executing a Return for books found on shelves that were supposedly issued).
3. Close the stocktake via `POST /library/stocktakes/{id}/close`.

## 4. Marking Missing
- Closing a stocktake does **not** automatically mark books as `missing`.
- The librarian must explicitly invoke `POST /mark-missing` on copies identified in the report to write the audit trail.
