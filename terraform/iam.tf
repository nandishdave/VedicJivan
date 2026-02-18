data "aws_caller_identity" "current" {}

# ══════════════════════════════════════════════
#  IAM — Frontend Deployer
# ══════════════════════════════════════════════

resource "aws_iam_user" "deployer" {
  name = "${lower(var.project_name)}-deployer"

  tags = {
    Project = var.project_name
  }
}

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
        Sid      = "S3ListBucket"
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = aws_s3_bucket.website.arn
      },
      {
        Sid      = "S3ManageObjects"
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"]
        Resource = "${aws_s3_bucket.website.arn}/*"
      }
    ]
  })
}

# CloudFront invalidation policy
resource "aws_iam_user_policy" "deployer_cloudfront" {
  name = "${lower(var.project_name)}-cloudfront-invalidate"
  user = aws_iam_user.deployer.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "CloudFrontInvalidation"
        Effect   = "Allow"
        Action   = ["cloudfront:CreateInvalidation"]
        Resource = aws_cloudfront_distribution.website.arn
      }
    ]
  })
}

# ECR + ECS deploy policy — allows GitHub Actions to push images and update service
resource "aws_iam_user_policy" "deployer_backend" {
  name = "${lower(var.project_name)}-backend-deploy"
  user = aws_iam_user.deployer.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ECRAuth"
        Effect   = "Allow"
        Action   = ["ecr:GetAuthorizationToken"]
        Resource = "*"
      },
      {
        Sid    = "ECRPush"
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload"
        ]
        Resource = aws_ecr_repository.api.arn
      },
      {
        Sid    = "ECSUpdateService"
        Effect = "Allow"
        Action = [
          "ecs:UpdateService",
          "ecs:DescribeServices",
          "ecs:DescribeTaskDefinition",
          "ecs:RegisterTaskDefinition"
        ]
        Resource = "*"
      },
      {
        Sid    = "PassRoleForECS"
        Effect = "Allow"
        Action = ["iam:PassRole"]
        Resource = [
          aws_iam_role.ecs_execution.arn,
          aws_iam_role.ecs_task.arn
        ]
      }
    ]
  })
}


# ══════════════════════════════════════════════
#  IAM — ECS Execution Role
#  (Used by ECS agent to pull images, fetch secrets, write logs)
# ══════════════════════════════════════════════

resource "aws_iam_role" "ecs_execution" {
  name = "${lower(var.project_name)}-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project = var.project_name
  }
}

# Attach the AWS-managed ECS task execution policy (ECR pull + CloudWatch logs)
resource "aws_iam_role_policy_attachment" "ecs_execution_policy" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Allow the execution role to read secrets from SSM Parameter Store
resource "aws_iam_role_policy" "ecs_execution_ssm" {
  name = "${lower(var.project_name)}-ecs-ssm"
  role = aws_iam_role.ecs_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ssm:GetParameters"]
        Resource = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter${local.ssm_prefix}/*"
      }
    ]
  })
}


# ══════════════════════════════════════════════
#  IAM — ECS Task Role
#  (Used by the running container for AWS API calls, if needed)
# ══════════════════════════════════════════════

resource "aws_iam_role" "ecs_task" {
  name = "${lower(var.project_name)}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project = var.project_name
  }
}
