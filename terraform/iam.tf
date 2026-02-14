# IAM User for GitHub Actions deployment
resource "aws_iam_user" "deployer" {
  name = "${lower(var.project_name)}-deployer"

  tags = {
    Project = var.project_name
  }
}

# Access key for the deployer user
resource "aws_iam_access_key" "deployer" {
  user = aws_iam_user.deployer.name
}

# S3 deployment policy — scoped to this bucket only
resource "aws_iam_user_policy" "deployer_s3" {
  name = "${lower(var.project_name)}-s3-deploy"
  user = aws_iam_user.deployer.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3ListBucket"
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.website.arn
      },
      {
        Sid    = "S3ManageObjects"
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.website.arn}/*"
      }
    ]
  })
}

# CloudFront invalidation policy — scoped to this distribution only
resource "aws_iam_user_policy" "deployer_cloudfront" {
  name = "${lower(var.project_name)}-cloudfront-invalidate"
  user = aws_iam_user.deployer.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "CloudFrontInvalidation"
        Effect = "Allow"
        Action = [
          "cloudfront:CreateInvalidation"
        ]
        Resource = aws_cloudfront_distribution.website.arn
      }
    ]
  })
}
