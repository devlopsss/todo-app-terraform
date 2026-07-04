resource "aws_secretsmanager_secret" "cognito_secret" {
  name                    = "${var.app_name}-cognito-secret-v2"
  description             = "Cognito app client credentials for ${var.app_name}"
  recovery_window_in_days = 7

  tags = {
    Name    = "${var.app_name}-cognito-secret"
    Project = var.app_name
  }
}

resource "aws_secretsmanager_secret_version" "cognito_secret_version" {
  secret_id = aws_secretsmanager_secret.cognito_secret.id
  secret_string = jsonencode({
    client_id     = var.cognito_client_id
    client_secret = var.cognito_client_secret
  })
}
