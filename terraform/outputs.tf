output "s3_bucket_name" {
  description = "S3 bucket name — use as S3_BUCKET_NAME GitHub secret"
  value       = aws_s3_bucket.website.id
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID — use as CLOUDFRONT_DISTRIBUTION_ID GitHub secret"
  value       = aws_cloudfront_distribution.website.id
}

output "cloudfront_domain" {
  description = "CloudFront domain — your website URL"
  value       = "https://${aws_cloudfront_distribution.website.domain_name}"
}

output "s3_website_endpoint" {
  description = "S3 static website endpoint (direct, without CloudFront)"
  value       = aws_s3_bucket_website_configuration.website.website_endpoint
}

output "deployer_access_key_id" {
  description = "IAM deployer access key ID — use as AWS_ACCESS_KEY_ID GitHub secret"
  value       = aws_iam_access_key.deployer.id
}

output "deployer_secret_access_key" {
  description = "IAM deployer secret key — use as AWS_SECRET_ACCESS_KEY GitHub secret"
  value       = aws_iam_access_key.deployer.secret
  sensitive   = true
}

output "aws_region" {
  description = "AWS region — use as AWS_REGION GitHub secret"
  value       = var.aws_region
}
