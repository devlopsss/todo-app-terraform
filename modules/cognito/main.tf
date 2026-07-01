resource "aws_cognito_user_pool" "todo_pool" {
  name = "${var.app_name}-userpool"

  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  tags = {
    Name    = "${var.app_name}-userpool"
    Project = var.app_name
  }
}

resource "aws_cognito_user_pool_client" "todo_client" {
  name         = "${var.app_name}-client"
  user_pool_id = aws_cognito_user_pool.todo_pool.id

  generate_secret = true

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]

  prevent_user_existence_errors = "ENABLED"
}
