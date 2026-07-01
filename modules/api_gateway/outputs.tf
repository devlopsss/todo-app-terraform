output "invoke_url" {
  description = "API Gateway invoke URL"
  value       = aws_api_gateway_stage.prod.invoke_url
}

output "api_id" {
  description = "API Gateway ID"
  value       = aws_api_gateway_rest_api.todo_api.id
}
