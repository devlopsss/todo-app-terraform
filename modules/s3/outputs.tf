output "bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.frontend.id
}

output "website_url" {
  description = "S3 static website URL"
  value       = aws_s3_bucket_website_configuration.frontend.website_endpoint
}
