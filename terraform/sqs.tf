# ══════════════════════════════════════════════
#  SQS — Kundli generation queue + DLQ
# ══════════════════════════════════════════════
#
# The API enqueues one message per kundli generation request. The
# kundli Lambda consumes them, runs Playwright + Resend, and AWS
# auto-deletes successful messages from the queue.
#
# A message goes to the DLQ after maxReceiveCount=3 redrives —
# at which point a CloudWatch alarm pages us (see cloudwatch.tf).

resource "aws_sqs_queue" "kundli_dlq" {
  name = "${local.name_prefix}-kundli-dlq"

  # 14-day max retention so we have time to inspect failed messages
  # before they age out of the DLQ.
  message_retention_seconds = 1209600

  tags = local.common_tags
}

resource "aws_sqs_queue" "kundli" {
  name = "${local.name_prefix}-kundli"

  # 15 min — must be >= the Lambda's max execution time so a slow job
  # (e.g. a month-scale unshakable scan) doesn't get redelivered to a
  # second Lambda invocation while the first is still working.
  visibility_timeout_seconds = 900

  # 4-day retention on the main queue. If something is stuck for
  # 4 days we have bigger problems than the message itself.
  message_retention_seconds = 345600

  # Long-polling reduces empty-receive costs and Lambda churn.
  receive_wait_time_seconds = 20

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.kundli_dlq.arn
    maxReceiveCount     = 3
  })

  tags = local.common_tags
}

output "kundli_queue_url" {
  description = "SQS queue URL for the kundli generation pipeline"
  value       = aws_sqs_queue.kundli.url
}

output "kundli_queue_arn" {
  description = "SQS queue ARN (used by the Lambda event source mapping)"
  value       = aws_sqs_queue.kundli.arn
}

output "kundli_dlq_arn" {
  description = "Dead-letter queue ARN"
  value       = aws_sqs_queue.kundli_dlq.arn
}
