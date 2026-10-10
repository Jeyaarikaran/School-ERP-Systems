# Library Rules & Configuration

This document outlines the operational rules and limit math applied in the Library module.

## 1. Member Limits & Blocks
Every checkout (Issue) must pass a strict validation chain based on the member's type (`student` or `staff`):
- **Max Books (`library.max_books`):** The member cannot exceed this count of concurrently open issues.
- **Max Renewals (`library.max_renewals`):** A copy cannot be renewed if this count is exceeded.
- **Overdue Count Block (`library.block_issue_if_overdue_count`):** Issue is blocked if the member has this many books overdue.
- **Unpaid Fines Block (`library.block_issue_if_unpaid_fines_over`):** Issue is blocked if the total outstanding (unpaid) library fines exceed this amount.

*Override:* A librarian with `library.override_limits` can force an issue despite these blocks by providing a mandatory reason (audited).

## 2. Overdue Fines Calculation
Fines are computed using a pure function when a book is returned late.
- **Rate (`library.fine_per_day`):** The base monetary rate per late day.
- **Grace Days (`library.fine_grace_days`):** Number of days after the due date before fines begin accruing.
- **Skip Holidays (`library.fine_skip_holidays`):** If true, weekends and dates in `school_calendar_days` marked as non-working are subtracted from the overdue days.
- **Cap (`library.fine_cap`):** The maximum fine amount. Can be a fixed amount or set to `book_price` to cap at the book's replacement value.
- **Rounding:** `Decimal HALF_UP` is used for all calculations.

## 3. Lost Book Fines
If a book is marked lost, the fine is assessed immediately.
- **Calculation:** `(book_price * library.lost_book_multiplier) + library.lost_processing_fee`.

## 4. Double Issue Prevention
The database physically prevents a copy from being checked out twice using a partial unique index:
`UNIQUE INDEX ON book_issues (copy_id) WHERE returned_at IS NULL AND status = 'issued'`
This guarantees safety even if the frontend fires 50 concurrent issue requests for the same scanner read.

## 5. Fine Ledger Integration
For students, Library Fines are instantly posted to the central Fee Ledger via `FeeChargeService`. 
- **Payment:** Paid by parents through the standard fee portal.
- **Waiver:** A librarian with `library.fines_waive` can waive a fine *only if* it has not been paid. Once paid, it must be handled as a standard fee refund.
