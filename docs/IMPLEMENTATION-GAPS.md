# Fase 4: execution integration status

## Implemented
- Original in-memory API remains unchanged for local demonstrations.
- Optional `app.persistent_api:app` routes to DynamoDB repository.
- Conditional DynamoDB writes for creation and state transitions.
- SQS publisher adapter and unit tests.
- Terraform HML draft (DynamoDB, SQS, DLQ), not applied.

## Required before deployment
- Map DynamoDB ConditionalCheckFailedException to HTTP 409, not HTTP 500.
- Introduce durable outbox or equivalent, idempotent SQS consumers, retries and DLQ redrive.
- Authenticate inter-service requests, use least-privilege IAM and AWS workload identity.
- Verify business rule: only paid/authorized orders may enter execution.
- Wire SQS publisher to committed state transitions without event loss.
- Propagate trace context and expose metrics, logs and health/readiness checks.
- Provision resources only after approved cost estimate and Terraform plan.
