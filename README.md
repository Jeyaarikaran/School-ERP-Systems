# EduCore ERP: Complete Stack Setup & Handover (Phase 11)

Welcome to the **EduCore ERP** system! This repository contains the complete implementation of the 11-Phase Architecture spanning the Next.js Admin portal, the Python FastAPI Backend, the Celery Background Workers, and the Flutter Mobile App.

This document serves as the final **Setup and Handover** guide.

## 🚀 Quick Start (Dockerized Development)

We have provided a unified `docker-compose.yml` that orchestrates the entire complex architecture locally.

1. **Ensure Docker Desktop is running.**
2. Open your terminal at the root of the project.
3. Run the following command:

```bash
docker-compose up --build
```

### What happens when you run this?
Docker will simultaneously spin up 7 isolated containers:
1. **`postgres`**: The PostgreSQL 16 database.
2. **`redis`**: The Redis 7 in-memory store (used for Rate Limiting, Revoked Tokens, and Celery Broker).
3. **`minio`**: A local AWS S3-compatible object storage bucket (for storing uploaded fee receipts and homework attachments).
4. **`api`**: The Python FastAPI backend running on `http://localhost:8000`.
5. **`celery_worker`**: The background worker threads consuming the `critical`, `notifications`, and `reports` queues.
6. **`celery_beat`**: The scheduler triggering the Transactional Outbox dispatcher (`SKIP LOCKED`) every 10 seconds.
7. **`admin`**: The Next.js Web Admin portal running on `http://localhost:3000`.

---

## 🛠️ Manual Database Initialization

If this is your first time booting the project, you need to apply the massive database schema containing all 241 tables across the 11 modules.

While the FastAPI container is running, execute Alembic migrations:

```bash
cd backend
alembic upgrade head
```

---

## 📱 Running the Flutter Mobile App

The mobile app cannot easily be run inside `docker-compose` as it requires an Android Emulator or iOS Simulator. 

1. Ensure you have the Flutter SDK installed.
2. Open an Android Emulator.
3. Run the app:

```bash
cd mobile
flutter pub get
flutter run
```

*Note on Localhost:* If running on an Android emulator, the API Client is configured to point to `http://10.0.2.2:8000` to reach your local Docker container.

---

## 🏗️ Architecture Map

Here is a quick map of where everything lives:

- **`admin/`**: The Next.js 14 App Router frontend. Contains the highly interactive Dashboards for Attendance, Marks, Fees, and Communication.
- **`backend/app/models/`**: The massive SQLAlchemy database schema enforcing the data models.
- **`backend/app/core/repository.py`**: The mathematical enforcer of Multi-Tenancy (Row-Level Security).
- **`backend/app/api/dependencies.py`**: The JWT and RBAC Permission Guard intercepting all traffic.
- **`mobile/lib/core/network/sync_worker.dart`**: The Offline-First Idempotency engine allowing teachers to take attendance without internet.

---

## 🛡️ Production Checklist before Go-Live

1. **Generate real cryptographic keys** for `JWT_SECRET_KEY` in the `.env` file.
2. **Swap MinIO for AWS S3** by updating the `S3_ENDPOINT_URL` environment variables.
3. **Replace the FakeGateway** with Razorpay production API keys.
4. **Deploy the Postgres DB** to a managed service like AWS RDS or GCP Cloud SQL to ensure automated backups and point-in-time recovery.

***

**Congratulations on the successful completion of the EduCore ERP Architecture!**
