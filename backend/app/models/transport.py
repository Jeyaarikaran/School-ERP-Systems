import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, ForeignKey, DateTime, Date, Boolean, Index, UniqueConstraint, Numeric, Integer, text, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, INT4RANGE, DATERANGE
from sqlalchemy.orm import relationship

from app.core.database import Base

class TransportBus(Base):
    __tablename__ = "transport_buses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    registration_no = Column(String, nullable=False)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)
    capacity = Column(Integer, nullable=False)
    fuel_type = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active") # active, maintenance, retired
    gps_device_id = Column(String, nullable=True) # reserved for future live-location tracking
    
    insurance_expiry = Column(Date, nullable=True)
    fitness_expiry = Column(Date, nullable=True)
    permit_expiry = Column(Date, nullable=True)
    pollution_expiry = Column(Date, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "registration_no", name="uq_transport_buses_registration"),
    )

class TransportCrewProfile(Base):
    __tablename__ = "transport_crew_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False) # driver, attendant
    license_number_enc = Column(String, nullable=True) # AES-GCM encrypted
    license_expiry = Column(Date, nullable=True)
    badge_no = Column(String, nullable=True)
    medical_fitness_expiry = Column(Date, nullable=True)
    police_verification_date = Column(Date, nullable=True)
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "staff_id", name="uq_transport_crew_profiles_staff"),
    )

class TransportBusCrew(Base):
    __tablename__ = "transport_bus_crew"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    bus_id = Column(UUID(as_uuid=True), ForeignKey("transport_buses.id", ondelete="CASCADE"), nullable=False)
    crew_profile_id = Column(UUID(as_uuid=True), ForeignKey("transport_crew_profiles.id", ondelete="CASCADE"), nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=True)
    
    # Exclusion constraints implemented in DB migrations (GiST index over daterange)

class TransportFeeZone(Base):
    __tablename__ = "transport_fee_zones"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    name_local = Column(String, nullable=True)

class TransportFeePlan(Base):
    __tablename__ = "transport_fee_plans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    zone_id = Column(UUID(as_uuid=True), ForeignKey("transport_fee_zones.id", ondelete="CASCADE"), nullable=False)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    annual_amount = Column(Numeric(12, 2), nullable=False)
    installments = Column(JSONB, nullable=False) # [{no, due_date, amount}]

class TransportStop(Base):
    __tablename__ = "transport_stops"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    name_local = Column(String, nullable=True)
    landmark = Column(String, nullable=True)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    fee_zone_id = Column(UUID(as_uuid=True), ForeignKey("transport_fee_zones.id", ondelete="SET NULL"), nullable=True)

class TransportRoute(Base):
    __tablename__ = "transport_routes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False, default="active")
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_transport_routes_code"),
    )

class TransportRouteStop(Base):
    __tablename__ = "transport_route_stops"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(UUID(as_uuid=True), ForeignKey("transport_routes.id", ondelete="CASCADE"), nullable=False)
    stop_id = Column(UUID(as_uuid=True), ForeignKey("transport_stops.id", ondelete="CASCADE"), nullable=False)
    sequence = Column(Integer, nullable=False)
    pickup_time = Column(String, nullable=True) # HH:MM
    drop_time = Column(String, nullable=True)
    
    __table_args__ = (
        UniqueConstraint("route_id", "sequence", name="uq_transport_route_stops_seq"),
    )

class TransportRouteAssignment(Base):
    __tablename__ = "transport_route_assignments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(UUID(as_uuid=True), ForeignKey("transport_routes.id", ondelete="CASCADE"), nullable=False)
    bus_id = Column(UUID(as_uuid=True), ForeignKey("transport_buses.id", ondelete="CASCADE"), nullable=False)
    trip_type = Column(String, nullable=False) # pickup, drop
    window = Column(INT4RANGE, nullable=False)
    effective_range = Column(DATERANGE, nullable=False)
    
    # DB Exclusion logic enforces no overlap per bus/time/date

class StudentTransport(Base):
    __tablename__ = "student_transport"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(UUID(as_uuid=True), ForeignKey("transport_routes.id", ondelete="CASCADE"), nullable=False)
    pickup_stop_id = Column(UUID(as_uuid=True), ForeignKey("transport_stops.id", ondelete="RESTRICT"), nullable=True)
    drop_stop_id = Column(UUID(as_uuid=True), ForeignKey("transport_stops.id", ondelete="RESTRICT"), nullable=True)
    usage = Column(String, nullable=False, default="both") # both, pickup_only, drop_only
    status = Column(String, nullable=False, default="active") # active, suspended, cancelled
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    __table_args__ = (
        Index("ix_student_transport_active", "student_id", "academic_year_id", postgresql_where=text("status = 'active'"), unique=True),
    )

class TransportTripRun(Base):
    __tablename__ = "transport_trip_runs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(UUID(as_uuid=True), ForeignKey("transport_routes.id", ondelete="CASCADE"), nullable=False)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("transport_route_assignments.id", ondelete="SET NULL"), nullable=True)
    bus_id = Column(UUID(as_uuid=True), ForeignKey("transport_buses.id", ondelete="CASCADE"), nullable=False)
    driver_profile_id = Column(UUID(as_uuid=True), ForeignKey("transport_crew_profiles.id", ondelete="RESTRICT"), nullable=False)
    attendant_profile_id = Column(UUID(as_uuid=True), ForeignKey("transport_crew_profiles.id", ondelete="SET NULL"), nullable=True)
    trip_type = Column(String, nullable=False) # pickup, drop
    run_date = Column(Date, nullable=False)
    status = Column(String, nullable=False, default="scheduled") # scheduled, started, completed, cancelled
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    delay_minutes = Column(Integer, nullable=True)
    delay_reason = Column(String, nullable=True)
    
    __table_args__ = (
        UniqueConstraint("route_id", "trip_type", "run_date", name="uq_transport_trip_runs"),
    )

class TransportBoardingEvent(Base):
    __tablename__ = "transport_boarding_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    trip_run_id = Column(UUID(as_uuid=True), ForeignKey("transport_trip_runs.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String, nullable=False) # boarded, alighted, absent_at_stop
    stop_id = Column(UUID(as_uuid=True), ForeignKey("transport_stops.id", ondelete="SET NULL"), nullable=True)
    occurred_at = Column(DateTime(timezone=True), nullable=False) # client time
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) # server time
    recorded_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    source = Column(String, nullable=False, default="manual") # manual, rfid, gps
    client_event_id = Column(String, nullable=False) # idempotent marker
    
    __table_args__ = (
        UniqueConstraint("trip_run_id", "client_event_id", name="uq_transport_boarding_events_client_id"),
    )
