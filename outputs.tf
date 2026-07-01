output "api_gateway_url" {
  description = "API Gateway invoke URL"
  value       = module.api_gateway.invoke_url
}

output "s3_website_url" {
  description = "S3 frontend website URL"
  value       = module.s3.website_url
}

output "cognito_user_pool_id" {
  description = "Cognito user pool ID"
  value       = module.cognito.user_pool_id
}

output "dynamodb_table_name" {
  description = "DynamoDB table name"
  value       = module.dynamodb.table_name
}
