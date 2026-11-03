# Execution HML infrastructure — proposal only

Creates one on-demand DynamoDB table and SQS queue with DLQ in us-east-1.
No Terraform apply has been executed. Run `terraform init`, `terraform plan`,
review expected costs, IAM and security posture, and obtain explicit approval
before `terraform apply`. This does not configure EKS IAM/IRSA, consumers,
application persistence or network permissions. AWS charges depend on usage.
