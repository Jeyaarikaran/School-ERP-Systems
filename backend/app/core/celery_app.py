from celery import Celery
import os

# Default to localhost Redis if not set
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")

celery_app = Celery(
    "erp_worker",
    broker=REDIS_URL,
    backend=REDIS_URL, # Stores task results
)

# Configuration matching ADR-002: Background Jobs
celery_app.conf.update(
    # Timezone
    timezone="Asia/Kolkata",
    enable_utc=True,
    
    # Retry and limits
    task_acks_late=True, # Ensure tasks are idempotent, only ack after successful completion
    task_reject_on_worker_lost=True,
    broker_connection_retry_on_startup=True,
    
    # Predefined Queues (Phase 1 Arch Docs)
    task_routes={
        "app.workers.notifications.*": {"queue": "notifications"},
        "app.workers.outbox_dispatcher.*": {"queue": "critical"},
        "app.workers.reports.*": {"queue": "reports"},
        "app.workers.imports.*": {"queue": "imports"},
    },
    
    # Schedule (Celery Beat)
    beat_schedule={
        "dispatch-outbox-every-10-seconds": {
            "task": "app.workers.outbox_dispatcher.process_outbox_events",
            "schedule": 10.0,
        },
    }
)

# Autodiscover tasks from the workers package
celery_app.autodiscover_tasks(["app.workers"])
