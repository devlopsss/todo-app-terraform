variable "app_name" {
  description = "Application name"
  type        = string
}

variable "lambda_role_arn" {
  description = "IAM role ARN for Lambda execution"
  type        = string
}

variable "secret_name" {
  description = "Secrets Manager secret name"
  type        = string
}

variable "dynamodb_table" {
  description = "DynamoDB table name"
  type        = string
}
