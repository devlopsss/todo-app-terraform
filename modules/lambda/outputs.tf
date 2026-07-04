output "function_arns" {
  description = "Map of Lambda alias ARNs — API Gateway uses these"
  value = {
    for k, v in aws_lambda_alias.prod : k => v.arn
  }
}

output "function_names" {
  description = "Map of Lambda function names"
  value = {
    for k, v in aws_lambda_function.functions : k => v.function_name
  }
}

output "function_versions" {
  description = "Map of current deployed versions"
  value = {
    for k, v in aws_lambda_function.functions : k => v.version
  }
}
