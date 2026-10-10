# GPS-Ready Design for Transport

This document outlines the architectural seams left in the Phase 9 Transport module to support live GPS tracking in the future, without building the actual ingestion pipeline now.

## Schema Hooks
- `transport_buses.gps_device_id`: Reserved string to map a physical GPS device to a vehicle.
- `transport_boarding_events.source`: Currently uses `manual` and `rfid`. The `gps` source is reserved for events generated via geofence proximity (e.g. "bus entered stop zone").
- `trip_run_id`: The primary foreign key intended for joining live location pings to a specific trip context.

## Planned `LocationProvider` Interface
Future iterations will introduce a `LocationProvider` interface to decouple GPS ingestion (from third-party vendors or mobile devices) from the core `TripRun` logic:
```python
class LocationProvider(Protocol):
    def post_location(self, trip_run_id: UUID, lat: Decimal, lon: Decimal, speed: Decimal, timestamp: datetime) -> None: ...
    def get_latest_location(self, trip_run_id: UUID) -> Optional[LocationPing]: ...
```

## Real-time Sync (WebSockets)
Live tracking will utilize the Phase 8 WebSocket infrastructure:
- **Channel Naming:** `trip:{trip_run_id}`
- **Isolation:** Subscriptions to this channel will be explicitly verified against `transport_route_assignments` to ensure only parents with an active `student_transport` record for that specific route and trip type can connect.

## Storage and Retention
- **Volume Math:** 1 ping every 10 seconds per bus (40 buses) = 240 pings/minute = ~14,400 pings/hour.
- **Storage Strategy:** Pings should be written to an ephemeral Redis stream or a time-series DB extension (e.g., TimescaleDB). Relational persistence is discouraged for raw pings.

## Privacy Considerations
- Geolocation tracking of minors is highly sensitive.
- Live tracking must immediately terminate when the `TripRun` status is marked `completed` or `cancelled`.
- Historic path lines must only be retained for compliance audits (e.g., 30 days) before aggressive pruning.
