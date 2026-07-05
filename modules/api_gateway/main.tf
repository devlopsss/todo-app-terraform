resource "aws_api_gateway_rest_api" "todo_api" {
  name        = "${var.app_name}-api"
  description = "Todo app REST API"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name    = "${var.app_name}-api"
    Project = var.app_name
  }
}

resource "aws_api_gateway_authorizer" "todo_authorizer" {
  name                             = "${var.app_name}-authorizer"
  rest_api_id                      = aws_api_gateway_rest_api.todo_api.id
  authorizer_uri                   = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${var.lambda_arns["todo_authorizer"]}/invocations"
  authorizer_result_ttl_in_seconds = 0
  type                             = "TOKEN"
  identity_source                  = "method.request.header.Authorization"
}

resource "aws_api_gateway_resource" "signup" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_rest_api.todo_api.root_resource_id
  path_part   = "signup"
}

resource "aws_api_gateway_resource" "confirm" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_rest_api.todo_api.root_resource_id
  path_part   = "confirm"
}

resource "aws_api_gateway_resource" "login" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_rest_api.todo_api.root_resource_id
  path_part   = "login"
}

resource "aws_api_gateway_resource" "create" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_rest_api.todo_api.root_resource_id
  path_part   = "create"
}

resource "aws_api_gateway_resource" "read" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_rest_api.todo_api.root_resource_id
  path_part   = "read"
}

resource "aws_api_gateway_resource" "update" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_rest_api.todo_api.root_resource_id
  path_part   = "update"
}

resource "aws_api_gateway_resource" "update_id" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_resource.update.id
  path_part   = "{todoId}"
}

resource "aws_api_gateway_resource" "delete" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_rest_api.todo_api.root_resource_id
  path_part   = "delete"
}

resource "aws_api_gateway_resource" "delete_id" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_resource.delete.id
  path_part   = "{todoId}"
}

locals {
  public_routes = {
    signup  = { resource_id = aws_api_gateway_resource.signup.id, http_method = "POST", lambda = "todo_signup" }
    confirm = { resource_id = aws_api_gateway_resource.confirm.id, http_method = "POST", lambda = "todo_confirm" }
    login   = { resource_id = aws_api_gateway_resource.login.id, http_method = "POST", lambda = "todo_login" }
  }

  protected_routes = {
    create    = { resource_id = aws_api_gateway_resource.create.id, http_method = "POST", lambda = "todo_create" }
    read      = { resource_id = aws_api_gateway_resource.read.id, http_method = "GET", lambda = "todo_read" }
    update_id = { resource_id = aws_api_gateway_resource.update_id.id, http_method = "PUT", lambda = "todo_update" }
    delete_id = { resource_id = aws_api_gateway_resource.delete_id.id, http_method = "DELETE", lambda = "todo_delete" }
  }
}

resource "aws_api_gateway_method" "public" {
  for_each      = local.public_routes
  rest_api_id   = aws_api_gateway_rest_api.todo_api.id
  resource_id   = each.value.resource_id
  http_method   = each.value.http_method
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "public" {
  for_each                = local.public_routes
  rest_api_id             = aws_api_gateway_rest_api.todo_api.id
  resource_id             = each.value.resource_id
  http_method             = aws_api_gateway_method.public[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${var.lambda_arns[each.value.lambda]}/invocations"

}

resource "aws_api_gateway_method" "protected" {
  for_each      = local.protected_routes
  rest_api_id   = aws_api_gateway_rest_api.todo_api.id
  resource_id   = each.value.resource_id
  http_method   = each.value.http_method
  authorization = "CUSTOM"
  authorizer_id = aws_api_gateway_authorizer.todo_authorizer.id

}

resource "aws_api_gateway_integration" "protected" {
  for_each                = local.protected_routes
  rest_api_id             = aws_api_gateway_rest_api.todo_api.id
  resource_id             = each.value.resource_id
  http_method             = aws_api_gateway_method.protected[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${var.lambda_arns[each.value.lambda]}/invocations"
}

resource "aws_lambda_permission" "public" {
  for_each      = local.public_routes
  statement_id  = "AllowAPIGateway-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_arns[each.value.lambda]
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.todo_api.id}/*/${each.value.http_method}/${each.key}"
}

resource "aws_lambda_permission" "protected" {
  for_each      = local.protected_routes
  statement_id  = "AllowAPIGateway-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_arns[each.value.lambda]
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.todo_api.id}/*/*"
}

resource "aws_lambda_permission" "authorizer" {
  statement_id  = "AllowAPIGatewayAuthorizer"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_arns["todo_authorizer"]
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.account_id}:${aws_api_gateway_rest_api.todo_api.id}/authorizers/${aws_api_gateway_authorizer.todo_authorizer.id}"
}

resource "aws_api_gateway_deployment" "todo_deployment" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id

  depends_on = [
    aws_api_gateway_integration.public,
    aws_api_gateway_integration.protected
  ]

  lifecycle {
    create_before_destroy = true
  }
}

# CloudWatch log group for API Gateway access logs
resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "API-Gateway-Execution-Logs_${aws_api_gateway_rest_api.todo_api.id}/prod"
  retention_in_days = 30

  tags = {
    Name    = "${var.app_name}-api-logs"
    Project = var.app_name
  }
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.todo_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.todo_api.id
  stage_name    = "prod"

  xray_tracing_enabled = true

  # Access logging — correct for REST API
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_logs.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      resourcePath   = "$context.resourcePath"
      status         = "$context.status"
      responseLength = "$context.responseLength"
      userAgent      = "$context.identity.userAgent"
    })
  }

  depends_on = [aws_cloudwatch_log_group.api_gateway_logs]

  tags = {
    Name    = "${var.app_name}-prod"
    Project = var.app_name
  }
}

# Throttling for REST API goes in method_settings
resource "aws_api_gateway_method_settings" "all" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  stage_name  = aws_api_gateway_stage.prod.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled        = true
    logging_level          = "INFO"
    data_trace_enabled     = false
    throttling_burst_limit = 50
    throttling_rate_limit  = 100
  }
}

# IAM role for API Gateway to write CloudWatch logs
resource "aws_iam_role" "api_gateway_cloudwatch" {
  name = "${var.app_name}-api-gateway-cloudwatch-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "apigateway.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "api_gateway_cloudwatch" {
  role       = aws_iam_role.api_gateway_cloudwatch.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

# Account-level setting — required once per AWS account
resource "aws_api_gateway_account" "main" {
  cloudwatch_role_arn = aws_iam_role.api_gateway_cloudwatch.arn

  depends_on = [aws_iam_role_policy_attachment.api_gateway_cloudwatch]
}
