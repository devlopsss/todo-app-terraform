output "user_pool_id" {
  description = "Cognito user pool ID"
  value       = aws_cognito_user_pool.todo_pool.id
}

output "user_pool_arn" {
  description = "Cognito user pool ARN"
  value       = aws_cognito_user_pool.todo_pool.arn
}

output "client_id" {
  description = "Cognito app client ID"
  value       = aws_cognito_user_pool_client.todo_client.id
}

output "client_secret" {
  description = "Cognito app client secret"
  value       = aws_cognito_user_pool_client.todo_client.client_secret
  sensitive   = true
}
