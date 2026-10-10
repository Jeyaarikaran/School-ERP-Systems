# Disaster Recovery (DR) Runbook

## Tier 1 Disaster: Database Corruption or Dropped Tables
**RTO (Recovery Time Objective):** 1 Hour
**RPO (Recovery Point Objective):** 5 Minutes

### Procedure (Point-in-Time Recovery - PITR)
1. Stop all web traffic and celery workers. Put Cloudflare in "Maintenance Mode".
2. Identify the exact UTC time of the destructive event (e.g., `2026-10-05 14:03:00 UTC`).
3. Using the cloud provider console (AWS RDS / GCP Cloud SQL), initiate a PITR clone of the production database to exactly 1 minute *before* the destructive event.
4. Verify the cloned database instance contains the intact data.
5. Update the `DATABASE_URL` environment variables in the production environment secrets to point to the new database instance.
6. Restart the backend API deployments and Celery workers.
7. Verify functionality and lift Maintenance Mode.
8. Delete the corrupted database instance once confirmation is complete.

## Tier 2 Disaster: Complete Region Outage (e.g., AWS us-east-1 down)
**RTO:** 4 Hours
**RPO:** 1 Hour (Cross-region backup frequency)

### Procedure
1. Declare a Tier 2 disaster to all stakeholders.
2. Spin up the standby Infrastructure-as-Code (Terraform) in the secondary region (e.g., `us-west-2`).
3. Restore the latest cross-region snapshot to a new DB instance.
4. Update DNS routing (Route53/Cloudflare) to point to the load balancer in the secondary region.
5. Deploy application containers to the new cluster.
6. Note: Any data written between the last cross-region snapshot and the outage is lost. Communicate this data loss window to schools.

## Tier 3 Disaster: Accidental Deletion of S3 Bucket (Documents)
**RTO:** 24 Hours
**RPO:** 24 Hours

### Procedure
1. S3 Versioning and MFA Delete MUST be enabled. If bypassed, proceed to restore from the daily cross-account AWS Backup vault.
2. Initiate a restore job from AWS Backup to a newly created bucket.
3. Update `AWS_S3_BUCKET` environment variable.

> **Testing Frequency:** PITR must be tested quarterly. Region failover must be tested annually.
