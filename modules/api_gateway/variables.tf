variable "app_name" {
  description = "Application name"
  type        = string
}

variable "lambda_arns" {
  description = "Map of Lambda function ARNs"
  type        = map(string)
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "account_id" {
  description = "AWS account ID"
  type        = string
}
