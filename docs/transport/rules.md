# Transport Rules & Configuration

This document outlines the capacity and compliance mathematics applied in the Transport module.

## 1. Capacity & Over-Enrollment Safety
Bus capacity is strictly enforced during student enrollment.
- **Available Seats:** Computed dynamically as `Bus.capacity - seat_reserve` (buffer setting) minus the count of currently active riders for the target Route and Trip Type (`pickup` or `drop`).
- **Concurrency Locking:** Enrollments utilize a `FOR UPDATE` lock on the `transport_route_assignments` row. If 50 parents try to claim the last 10 seats simultaneously, the database guarantees exactly 10 will succeed and 40 will receive `ROUTE_FULL`.

## 2. Constraint Exclusions
To prevent logistical impossibilities, the database utilizes PostgreSQL `EXCLUDE USING GIST` constraints over `DATERANGE` and `INT4RANGE`:
- **Bus Overlap:** A specific bus cannot be assigned to two routes covering overlapping time windows on the same dates.
- **Crew Overlap:** A driver cannot be assigned to two active buses with overlapping date ranges.
- **Double Crew:** A bus cannot have two primary drivers with overlapping valid date ranges.

## 3. Compliance Blocking
Assets and Crew must remain legally compliant to operate.
- **Checks:** Before assigning a bus, or before a driver can `start` a Trip Run, the system validates `fitness_expiry`, `insurance_expiry`, `permit_expiry`, and `license_expiry`.
- **Block:** If any document is expired past midnight today, the action is blocked with `COMPLIANCE_EXPIRED`.
- **Override:** Transport Admin with `transport.override_compliance` can force the trip to start by supplying a logged reason.

## 4. Transport Fee Mapping
Enrollment directly hooks into the Fee Module.
- Creating an enrollment instantly creates fee items (`FeeChargeService.post_adhoc_charge`) mapped to the zone's `transport_fee_plans`.
- If a route is changed or suspended, all **UNPAID** future transport fee installments are automatically cancelled (`cancel_charges_by_reference`).
- **No Pro-Rata Auto-Refunds:** Any already **PAID** transport fees are completely untouched by the system. The admin receives a notification of the paid balance to manually issue a refund or credit note in Phase 7. This prevents automated runaway accounting errors.
