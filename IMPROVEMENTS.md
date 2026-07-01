# Future Improvements

## Security
- [ ] Add CloudFront in front of S3 for HTTPS/TLS support
      - Requires: ACM certificate + CloudFront distribution
      - Cost: ~$1/month
      - Terraform resource: aws_cloudfront_distribution

- [ ] Add WAF to API Gateway
      - Protects against SQL injection, XSS, bot traffic
      - Terraform resource: aws_wafv2_web_acl

- [ ] Add custom domain name to API Gateway
      - Enables TLS policy configuration
      - Requires: Route 53 hosted zone + ACM certificate

## Architecture
- [ ] Move to VPC for Lambda and DynamoDB
      - Adds network-level isolation
      - Terraform resource: aws_vpc

- [ ] Add token refresh flow
      - Use Cognito refresh token to silently renew expired sessions
      - Avoids forcing users to re-login every hour

## Monitoring
- [ ] Add CloudWatch alarms
      - Alert on Lambda errors > threshold
      - Alert on API Gateway 4xx/5xx spikes
      - Terraform resource: aws_cloudwatch_metric_alarm

- [ ] Add AWS X-Ray tracing end to end
      - Already enabled on API Gateway
      - Needs enabling on Lambda functions
