terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

variable "environment" {
  type    = string
  default = "hml"
  validation {
    condition     = var.environment == "hml"
    error_message = "This stack is restricted to hml."
  }
}
variable "aws_region" {
  type    = string
  default = "us-east-1"
}
variable "tags" {
  type    = map(string)
  default = {}
}
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = merge({ Project = "oficina", Environment = var.environment, ManagedBy = "terraform" }, var.tags)
  }
}
resource "aws_dynamodb_table" "execution" {
  name         = "oficina-execution-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"
  attribute {
    name = "order_id"
    type = "S"
  }
  point_in_time_recovery { enabled = false }
}
resource "aws_sqs_queue" "execution_dlq" {
  name                      = "oficina-execution-${var.environment}-dlq"
  message_retention_seconds = 1209600
  sqs_managed_sse_enabled   = true
}
resource "aws_sqs_queue" "execution" {
  name                       = "oficina-execution-${var.environment}"
  visibility_timeout_seconds = 60
  sqs_managed_sse_enabled    = true
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.execution_dlq.arn
    maxReceiveCount     = 5
  })
}
output "execution_table_name" { value = aws_dynamodb_table.execution.name }
output "execution_queue_url" { value = aws_sqs_queue.execution.url }
output "execution_dlq_url" { value = aws_sqs_queue.execution_dlq.url }
