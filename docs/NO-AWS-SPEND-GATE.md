# Zero incremental AWS spend policy (Fase 4)

User constraint: **do not exceed AWS free usage / incur any incremental AWS charge**.

**No AWS provisioning is authorized** by this policy. Do not run Terraform apply,
AWS CLI resource creation, or enable GitHub Actions deployment until a verified
cost assessment and explicit approval establish a safe path.

Important:
- AWS Free Tier eligibility is account-specific, service-specific and time-limited.
- An existing EKS cluster, EC2 worker nodes, NAT gateways, public IPv4,
  load balancers, CloudWatch, RDS, and data transfer may already incur charges.
- AWS Budgets alerts do **not** impose a hard spending cap.
- DynamoDB and SQS can have free usage allowances, but zero cost is not
  guaranteed by selecting on-demand billing or staying below a nominal quota.
- Terraform plan does not prove a zero-dollar AWS bill.

## Zero-spend development path
1. Develop and test FastAPI services with SQLite and mocked AWS clients.
2. Run local DynamoDB via container or mock (no AWS account calls).
3. Use LocalStack or mocked SQS locally; validate retries, idempotency and DLQ logic.
4. Validate Docker builds and CI unit tests on GitHub Actions subject to GitHub quotas.
5. Use local Kubernetes (kind/k3d) for deployment verification.
6. Document AWS Terraform as optional reference only; never auto-apply.
7. Require cost explorer/account eligibility and a concrete plan before any AWS apply.

## Remaining evidence
Local tests and mocked integrations are **not evidence of live AWS deployment**.
Document this limitation transparently in the FIAP submission.
