# Transport Data Privacy Policy

## 1. Principle of Minimization
Transport data involves the highly sensitive location and travel patterns of minors. The system is designed to collect and expose the absolute minimum data required to ensure student safety and logistical efficiency.

## 2. GPS and Location Data
- Core transport operations do **not** require live GPS data. Boarding events act as discrete checkpoints.
- If GPS tracking is enabled in the future (via `LocationProvider`), live tracking streams are strictly ephemeral.
- Connections to the WebSocket tracking channel (`trip:{id}`) enforce authorization at the connection layer. Only parents with an active `student_transport` record for the exact route and trip type can subscribe.
- Live tracking ceases immediately when the `trip_run` status changes to `completed` or `cancelled`.

## 3. Data Retention and Pruning
- **Boarding Events (`transport_boarding_events`):** Kept for a default of 12 months for compliance and dispute resolution.
- A scheduled Celery Beat job (`transport_prune_boarding_events`) automatically deletes boarding events older than the 12-month threshold.
- Historic pathing data (GPS pings, if ingested) must not be stored in the relational database. It should reside in a time-series database with an aggressive TTL (e.g., 30 days).

## 4. Exposure to Crew (Drivers & Attendants)
- Drivers and Attendants are granted access to a manifest strictly scoped to their assigned run for the day.
- The manifest displays the student's name, class, stop, and emergency contact details.
- Guardian profile information, addresses, and full contact sheets are entirely masked and inaccessible to transport crew.

## 5. Security of Crew Data
- Driver license numbers are AES-GCM encrypted at rest (`license_number_enc`).
- By default, licenses are returned masked (e.g., `********1234`).
- Unmasking requires the explicit `transport.view_sensitive` permission, and every full-text read is permanently audited.
