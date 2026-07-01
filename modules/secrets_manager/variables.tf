variable "app_name" {
  description = "Application name"
  type        = string
}

variable "cognito_client_id" {
  description = "Cognito app client ID"
  type        = string
}

variable "cognito_client_secret" {
  description = "Cognito app client secret"
  type        = string
  sensitive   = true
}
