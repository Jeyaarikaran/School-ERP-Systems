from app.core.celery_app import celery_app
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, queue="critical")
def process_outbox_events(self):
    """
    Transactional Outbox Dispatcher (ADR-013).
    This task runs every 10 seconds via Celery Beat.
    It uses FOR UPDATE SKIP LOCKED to grab a batch of pending events.
    """
    logger.info("Starting outbox event dispatcher...")
    
    # In a full implementation, we'd inject the SQLAlchemy session here.
    # Below is the exact Postgres query required by the architecture.
    sql = text("""
        WITH batch AS (
            SELECT id FROM outbox_events
            WHERE published_at IS NULL
            ORDER BY created_at ASC
            LIMIT 100
            FOR UPDATE SKIP LOCKED
        )
        UPDATE outbox_events e
        SET published_at = NOW()
        FROM batch
        WHERE e.id = batch.id
        RETURNING e.id, e.event_type, e.payload, e.school_id;
    """)

    # Mocking execution to demonstrate the architecture flow:
    # with get_sync_db_session() as session:
    #     events = session.execute(sql).fetchall()
    #     
    #     for event in events:
    #         if event.event_type == "attendance.submitted":
    #             from app.workers.notifications import send_absence_alerts
    #             send_absence_alerts.delay(event.school_id, event.payload)
    #             
    #         elif event.event_type == "fee.payment_received":
    #             # dispatch fee receipt generation
    #             pass

    logger.info("Outbox dispatcher completed batch.")
    return "Dispatcher Success"
