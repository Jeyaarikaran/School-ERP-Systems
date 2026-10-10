# Runbook: Transport Compliance Management

**Context:** Transport assets (Buses) and crew (Drivers) must maintain valid documentation. If documents expire, the system enforces a hard stop on operations.

## Proactive Management
1. The scheduled job `transport_compliance_check` runs nightly.
2. It generates `transport.document_expiring` events at 30 days, 7 days, and 0 days prior to expiry.
3. Transport Admin reviews the `GET /transport/compliance` endpoint weekly to upload renewed documents before expiration.

## Reactive Block (Day-of Expiry)
If a document expires and is not updated:
1. The driver attempts to tap `Start Trip` on their mobile device.
2. The API rejects the request with `COMPLIANCE_EXPIRED`.
3. The driver contacts the Transport Admin.
4. **Resolution A:** Admin updates the expiry dates on the Bus or Crew profile immediately. Driver retries.
5. **Resolution B (Emergency):** Admin utilizes their `transport.override_compliance` permission to force-start the trip run on the driver's behalf, providing a legally mandated audit reason.
