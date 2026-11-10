# Fase 4 — HML capacity and cost gate

## Proposed resources
- Reuse existing EKS HML and existing RDS PostgreSQL instance where feasible.
- Separate Billing database/schema and restricted credentials on RDS; do not grant OS service access.
- Execution DynamoDB PAY_PER_REQUEST (no provisioned capacity), PITR disabled for cost control in HML.
- SQS queue + DLQ with AWS-managed SSE.
- Kubernetes Deployments and Services, no additional public load balancer by default.

## Before apply
1. Collect current AWS Cost Explorer baseline and EKS node allocatable/requested CPU and memory.
2. Run Terraform plan and inspect incremental resources and IAM policies.
3. Estimate DynamoDB read/write/storage, SQS requests, RDS storage/connections and EKS capacity.
4. Confirm whether existing 2 x t3.micro nodes can host additional pods; do not assume they can.
5. Define a monthly spend ceiling, budget alerts and owner.
6. Obtain explicit approval for the estimated monthly amount before provisioning.

## Important
This is not an AWS price quotation: no live pricing, actual workloads or AWS billing
data have been consulted. There is **no permission to apply** based on this file alone.
