# ── CloudWatch Log Group ──
# Collects logs from the FastAPI container.

resource "aws_cloudwatch_log_group" "api" {
  name              = "/ecs/${lower(var.project_name)}-api"
  retention_in_days = 7

  tags = {
    Project = var.project_name
  }
}
