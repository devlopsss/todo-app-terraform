locals {
  functions = {
    todo_create     = { handler = "lambda_function.lambda_handler", has_env = false, timeout = 10, memory = 128 }
    todo_read       = { handler = "lambda_function.lambda_handler", has_env = false, timeout = 10, memory = 128 }
    todo_update     = { handler = "lambda_function.lambda_handler", has_env = false, timeout = 10, memory = 128 }
    todo_delete     = { handler = "lambda_function.lambda_handler", has_env = false, timeout = 10, memory = 128 }
    todo_authorizer = { handler = "lambda_function.lambda_handler", has_env = false, timeout = 5,  memory = 128 }
    todo_signup     = { handler = "lambda_function.lambda_handler", has_env = true,  timeout = 15, memory = 256 }
    todo_confirm    = { handler = "lambda_function.lambda_handler", has_env = true,  timeout = 15, memory = 256 }
    todo_login      = { handler = "lambda_function.lambda_handler", has_env = true,  timeout = 15, memory = 256 }
  }
}

data "archive_file" "lambda_zips" {
  for_each    = local.functions
  type        = "zip"
  source_dir  = "${path.module}/functions/${each.key}"
  output_path = "${path.module}/functions/${each.key}.zip"
}

resource "aws_lambda_function" "functions" {
  for_each         = local.functions
  function_name    = "${var.app_name}-${each.key}"
  role             = var.lambda_role_arn
  handler          = each.value.handler
  runtime          = "python3.12"
  filename         = data.archive_file.lambda_zips[each.key].output_path
  source_code_hash = data.archive_file.lambda_zips[each.key].output_base64sha256
  timeout          = each.value.timeout
  memory_size      = each.value.memory

  # Enable versioning — required for aliases
  publish = true

  dynamic "environment" {
    for_each = each.value.has_env ? [1] : []
    content {
      variables = {
        SECRET_NAME = var.secret_name
      }
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda_logs]

  tags = {
    Name    = "${var.app_name}-${each.key}"
    Project = var.app_name
  }
}

# Lambda alias — points to latest version
# API Gateway uses this alias, not the function directly
resource "aws_lambda_alias" "prod" {
  for_each         = local.functions
  name             = "prod"
  function_name    = aws_lambda_function.functions[each.key].function_name
  function_version = aws_lambda_function.functions[each.key].version

  lifecycle {
    create_before_destroy = true
  }
}

# CloudWatch log groups — 30 day retention
resource "aws_cloudwatch_log_group" "lambda_logs" {
  for_each          = local.functions
  name              = "/aws/lambda/${var.app_name}-${each.key}"
  retention_in_days = 30

  tags = {
    Name    = "${var.app_name}-${each.key}-logs"
    Project = var.app_name
  }
}
