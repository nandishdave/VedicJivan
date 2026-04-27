# ══════════════════════════════════════════════
#  Lambda — Kundli PDF Worker
# ══════════════════════════════════════════════
#
# Container-image Lambda that consumes the kundli SQS queue, renders
# the PDF with Playwright (headless Chromium), emails it via Resend,
# and writes the final status back to MongoDB.
#
# Why container image, not zip:
#   * Playwright + Chromium is ~600 MB compressed — well over the
#     250 MB zip ceiling but inside the 10 GB image ceiling.
#   * Same Dockerfile.lambda runs locally (`docker run -it ...`) for
#     interactive debugging.
#
# Sizing: 2048 MB / 5 min. Headless Chromium needs ~700 MB - 1.5 GB
# per render; 2048 leaves headroom and gets us 2x vCPU
# (Lambda gives ~1 vCPU per 1769 MB).

# ── ECR repo for the worker image ────────────────────────────────────────────

resource "aws_ecr_repository" "kundli_worker" {
  name                 = "${local.name_prefix}-kundli-worker"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = local.common_tags
}

resource "aws_ecr_lifecycle_policy" "kundli_worker" {
  repository = aws_ecr_repository.kundli_worker.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = { type = "expire" }
      }
    ]
  })
}

# ── IAM role for the Lambda ──────────────────────────────────────────────────

resource "aws_iam_role" "kundli_worker_lambda" {
  name = "${local.name_prefix}-kundli-worker-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })

  tags = local.common_tags
}

# CloudWatch Logs write
resource "aws_iam_role_policy_attachment" "kundli_worker_basic" {
  role       = aws_iam_role.kundli_worker_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# SQS receive + delete on the kundli queue (NOT the DLQ — Lambda
# never reads from the DLQ; redrive is automatic).
resource "aws_iam_role_policy" "kundli_worker_sqs" {
  name = "${local.name_prefix}-kundli-worker-sqs"
  role = aws_iam_role.kundli_worker_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:ChangeMessageVisibility",
        ]
        Resource = aws_sqs_queue.kundli.arn
      }
    ]
  })
}

# ── CloudWatch Log Group ─────────────────────────────────────────────────────
# Created in advance so the retention policy applies from day 1.

resource "aws_cloudwatch_log_group" "kundli_worker" {
  name              = "/aws/lambda/${local.name_prefix}-kundli-worker"
  retention_in_days = 7

  tags = local.common_tags
}

# ── Lambda function ──────────────────────────────────────────────────────────

#
# BOOTSTRAP NOTE: On first apply this resource will fail because
# `:latest` does not yet exist in the newly-created ECR repo. Sequence:
#
#   1. `terraform apply -target=aws_ecr_repository.kundli_worker` — repo exists
#   2. From `api/`: build + push the initial image:
#        aws ecr get-login-password --region ap-south-1 | \
#          docker login --username AWS --password-stdin <ecr-url>
#        docker build -t <ecr-url>:latest -f Dockerfile.lambda --platform linux/amd64 .
#        docker push <ecr-url>:latest
#   3. `terraform apply` — Lambda function creates successfully
#   4. CI takes over from here; every deploy rolls a new image via
#      `aws lambda update-function-code` in `.github/workflows/deploy-api.yml`.
#
resource "aws_lambda_function" "kundli_worker" {
  function_name = "${local.name_prefix}-kundli-worker"
  role          = aws_iam_role.kundli_worker_lambda.arn

  package_type = "Image"
  image_uri    = "${aws_ecr_repository.kundli_worker.repository_url}:latest"

  memory_size = 2048
  timeout     = 300 # must match SQS visibility_timeout_seconds in sqs.tf

  environment {
    variables = {
      # MONGODB_URI / RESEND_API_KEY / JWT_SECRET are baked into the
      # Lambda env at apply time (Lambda has no live-SSM-lookup feature
      # like ECS task secrets). A future SSM rotation requires a new
      # `terraform apply` or `aws lambda update-function-configuration`.
      MONGODB_URI    = data.aws_ssm_parameter.kundli_mongodb_uri.value
      RESEND_API_KEY = data.aws_ssm_parameter.kundli_resend_api_key.value
      JWT_SECRET     = data.aws_ssm_parameter.kundli_jwt_secret.value
      EMAIL_FROM     = "VedicJivan <noreply@nandishdave.world>"
      FRONTEND_URL   = "https://${local.frontend_domain}"
      # AWS_REGION is auto-set by the Lambda runtime — don't override.
      # The Lambda only CONSUMES from SQS via the event source mapping,
      # so it doesn't need KUNDLI_QUEUE_URL (only the API producer does).
      PDF_RENDERER = "playwright"
      APP_ENV      = local.env == "prod" ? "production" : local.env
    }
  }

  # Re-deploy when CI updates the image (deploy-api.yml flips the
  # `latest` tag; we use `image_uri` here pointing at `latest`, so
  # updating function-code via `aws lambda update-function-code`
  # in CI is what actually rolls a new build).
  lifecycle {
    ignore_changes = [image_uri]
  }

  depends_on = [
    aws_iam_role_policy_attachment.kundli_worker_basic,
    aws_cloudwatch_log_group.kundli_worker,
  ]

  tags = local.common_tags
}

# ── SQS → Lambda event source mapping ────────────────────────────────────────

resource "aws_lambda_event_source_mapping" "kundli_sqs" {
  event_source_arn = aws_sqs_queue.kundli.arn
  function_name    = aws_lambda_function.kundli_worker.arn

  # batch_size = 1 — one render per invocation. Better isolation
  # (one bad message can't stall siblings), simpler partial-failure
  # handling, fits our 10-15/day volume comfortably.
  batch_size = 1

  function_response_types = ["ReportBatchItemFailures"]
}

# ── Read SSM secrets at apply time so they bake into Lambda env ──────────────
# Lambda env vars are baked at deploy time (no live SSM lookup like
# ECS), so we read here. Mark `data` not `resource` so we don't try
# to create them — they're already created by secrets.tf.

data "aws_ssm_parameter" "kundli_mongodb_uri" {
  name = "${local.ssm_prefix}/MONGODB_URI"
}

data "aws_ssm_parameter" "kundli_resend_api_key" {
  name = "${local.ssm_prefix}/RESEND_API_KEY"
}

data "aws_ssm_parameter" "kundli_jwt_secret" {
  name = "${local.ssm_prefix}/JWT_SECRET"
}

output "kundli_worker_lambda_name" {
  description = "Lambda function name (used by CI to push new image versions)"
  value       = aws_lambda_function.kundli_worker.function_name
}

output "kundli_worker_ecr_url" {
  description = "ECR repo URL for the kundli worker image"
  value       = aws_ecr_repository.kundli_worker.repository_url
}
