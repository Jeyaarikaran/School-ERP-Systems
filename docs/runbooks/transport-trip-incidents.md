# Runbook: Transport Trip Incidents

**Context:** Handling on-road delays, breakdowns, or trip cancellations dynamically to ensure parents are informed immediately without manual phone trees.

## Scenario A: Heavy Traffic / Minor Delay
1. Driver taps "Report Delay" on their app.
2. API call: `POST /transport/trip-runs/{id}/delay` (e.g. `delay_minutes: 15`, `reason: heavy_traffic`).
3. System instantly dispatches `transport.trip_delayed` notifications to all parents with active students mapped to this specific run.
4. Parent app dashboard updates ETA dynamically.

## Scenario B: Vehicle Breakdown / Trip Cancelled Mid-Route
1. Driver is unable to continue. Transport Admin takes over.
2. Admin executes `POST /transport/trip-runs/{id}/cancel`.
3. System dispatches `transport.trip_cancelled` notifications.
4. Admin creates an ad-hoc Route Assignment for a backup bus to cover the remaining stops, issuing a new `trip_run`.

## Scenario C: Offline Mobile Device
1. Driver's mobile connection drops during boarding.
2. Driver continues scanning RFID or tapping manual boardings.
3. App queues events locally.
4. Upon reconnection, app flushes batch via `POST /transport/trip-runs/{id}/events`.
5. Database utilizes `client_event_id` to deduplicate any retries and processes the batch atomically. Out-of-sequence events (alight before board) are flagged with `warnings` rather than failing the sync.
