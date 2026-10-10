# Terraform / Infrastructure as Code (IaC) Plan

## Overview
This document outlines the planned infrastructure architecture for the School ERP backend. The infrastructure will be managed via Terraform to ensure reproducibility and consistency across environments (Staging, Production).

## Cloud Provider (Target: AWS)

### 1. Networking (VPC)
- **VPC:** 10.0.0.0/16
- **Public Subnets:** For Load Balancers and NAT Gateways.
- **Private Subnets:** For Application Servers (ECS/EKS), Redis, and Database.

### 2. Compute (ECS Fargate)
- **API Service:** Task definition running the FastAPI container. Auto-scaling target based on CPU (70%) and Memory (80%).
- **Celery Worker Service:** Task definition for background jobs. Scales based on queue length (via CloudWatch custom metrics).
- **Celery Beat Service:** Singleton task definition (1 instance max) for cron scheduling.

### 3. Data Tier
- **Relational Database:** Amazon RDS for PostgreSQL 16. Multi-AZ deployment for Production. 
- **Connection Pooling:** PgBouncer sidecar container or RDS Proxy to manage connection limits (max 200).
- **In-Memory Store:** Amazon ElastiCache for Redis (Cluster mode disabled, single shard with replica for failover).

### 4. Storage & CDN
- **Blob Storage:** Amazon S3 for document uploads, homework photos, and reports.
- **CDN:** Cloudflare (or CloudFront) in front of the Application Load Balancer to cache static assets and mitigate DDoS attacks.

### 5. Security & Observability
- **IAM:** Principle of least privilege. ECS Task execution roles restricted strictly to necessary S3 buckets and KMS keys.
- **Secrets:** AWS Secrets Manager for DB passwords, API keys (Sentry, AI providers), and JWT signing keys.
- **Logs:** FireLens/CloudWatch for container logs, exported to an external aggregator (e.g., Datadog or ELK) if necessary.

## Rollout Pipeline
1. `terraform plan` executes automatically on PR creation.
2. Manual approval required before `terraform apply` on the `main` branch.
3. State stored remotely in an S3 bucket with DynamoDB state locking.
