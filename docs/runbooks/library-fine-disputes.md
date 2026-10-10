# Runbook: Library Fine Disputes

**Context:** A student or parent disputes a library fine that has already been generated (e.g., claiming the book was returned on time but not scanned, or disputing the damage fee).

## Scenario A: Fine is UNPAID
If the parent has not yet paid the fine in the fee portal:
1. Librarian verifies the claim.
2. Librarian executes `POST /library/fines/{id}/waive` with a required `waive_reason`.
3. **Under the hood:** The system automatically calls `cancel_charges_by_reference` in the Fee Module, destroying the outstanding fee charge on the student's ledger.

## Scenario B: Fine is already PAID
If the parent has already paid the fine via cash or payment gateway:
1. Librarian attempts `POST /library/fines/{id}/waive`.
2. The system **REJECTS** the waiver with `FINE_ALREADY_PAID`.
3. The librarian must instruct the parent to seek a formal refund.
4. An accountant navigates to the Fee Module and processes a `refund_request` against the paid fee item to ensure the financial ledger balances.
