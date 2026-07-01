resource "aws_dynamodb_table" "todo_table" {
  name         = "${var.app_name}-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "userId"
  range_key    = "todoId"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "todoId"
    type = "S"
  }

  # Encryption at rest using AWS managed key
  server_side_encryption {
    enabled = true
  }

  # Point-in-time recovery — restore to any second in last 35 days
  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name        = "${var.app_name}-table"
    Environment = "prod"
    Project     = var.app_name
  }
}
