variable "app_name" {
  description = "Application name"
  type        = string
}

variable "dynamodb_arn" {
  description = "DynamoDB table ARN"
  type        = string
}

variable "cognito_arn" {
  description = "Cognito user pool ARN"
  type        = string
}

variable "secret_arn" {
  description = "Secrets Manager secret ARN"
  type        = string
}
