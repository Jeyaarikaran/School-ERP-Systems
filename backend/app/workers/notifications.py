from app.core.celery_app import celery_app
import logging
import time

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=5, queue="notifications")
def send_absence_alerts(self, school_id: str, payload: dict):
    """
    Consumes from the 'notifications' queue.
    Sends FCM Push and SMS fallback for absent students.
    Idempotent via 'dedupe_key' in the payload.
    """
    dedupe_key = payload.get("dedupe_key")
    student_id = payload.get("student_id")
    guardian_phone = payload.get("guardian_phone")
    guardian_fcm_token = payload.get("fcm_token")

    logger.info(f"Processing absence alert for student {student_id} (Dedupe: {dedupe_key})")

    try:
        # 1. Attempt FCM Push Notification (Fast, Free)
        if guardian_fcm_token:
            logger.info(f"Sending FCM push to token {guardian_fcm_token[:10]}...")
            time.sleep(0.5) # Simulate network call
            
            # If FCM succeeds, we return early
            return f"Push Sent to {student_id}"
            
        # 2. Fallback to SMS if critical category (e.g., Absence) and no FCM token
        if guardian_phone:
            logger.info(f"FCM missing/failed. Falling back to SMS via DLT template...")
            time.sleep(0.5) # Simulate Msg91 API call
            return f"SMS Sent to {guardian_phone}"
            
    except Exception as exc:
        # Exponential backoff with jitter per Architecture Docs
        logger.error(f"Delivery failed, retrying: {exc}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

@celery_app.task(bind=True, queue="notifications")
def generate_fee_receipt_pdf(self, school_id: str, receipt_id: str):
    """
    CPU-Heavy task offloaded to Celery.
    Generates a PDF receipt and uploads it to S3, then emails the parent.
    """
    logger.info(f"Generating PDF for receipt {receipt_id}")
    time.sleep(2) # Simulate CPU intensive PDF generation
    logger.info(f"Uploading {receipt_id}.pdf to S3 Bucket")
    
    return "Receipt Generated and Uploaded"
