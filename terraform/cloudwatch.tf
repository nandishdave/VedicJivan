# ── CloudWatch Log Groups ──

# ECS container logs
resource "aws_cloudwatch_log_group" "api" {
  name              = "/ecs/${lower(var.project_name)}-api"
  retention_in_days = 7

  tags = {
    Project = var.project_name
  }
}

# API Gateway access logs
resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/apigateway/${lower(var.project_name)}-api"
  retention_in_days = 7

  tags = {
    Project = var.project_name
  }
}


# ══════════════════════════════════════════════
#  SNS Topic — Alarm Notifications (email)
# ══════════════════════════════════════════════

resource "aws_sns_topic" "alarms" {
  name = "${lower(var.project_name)}-alarms"

  tags = {
    Project = var.project_name
  }
}

resource "aws_sns_topic_subscription" "alarm_email" {
  topic_arn = aws_sns_topic.alarms.arn
  protocol  = "email"
  endpoint  = var.alarm_email
}


# ══════════════════════════════════════════════
#  CloudWatch Alarms (within free tier: 10 alarms)
# ══════════════════════════════════════════════

# 1. ECS — Service has 0 running tasks (service is DOWN)
resource "aws_cloudwatch_metric_alarm" "ecs_no_running_tasks" {
  alarm_name          = "${lower(var.project_name)}-ecs-no-running-tasks"
  alarm_description   = "CRITICAL: API has 0 running tasks — service is down"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 1
  metric_name         = "RunningTaskCount"
  namespace           = "ECS/ContainerInsights"
  period              = 60
  statistic           = "Average"
  threshold           = 1
  treat_missing_data  = "breaching"

  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = aws_ecs_service.api.name
  }

  alarm_actions = [aws_sns_topic.alarms.arn]
  ok_actions    = [aws_sns_topic.alarms.arn]

  tags = {
    Project = var.project_name
  }
}

# 2. ECS — High CPU (>90% for 5 min)
resource "aws_cloudwatch_metric_alarm" "ecs_high_cpu" {
  alarm_name          = "${lower(var.project_name)}-ecs-high-cpu"
  alarm_description   = "WARNING: ECS CPU utilization above 90%"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 90

  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = aws_ecs_service.api.name
  }

  alarm_actions = [aws_sns_topic.alarms.arn]
  ok_actions    = [aws_sns_topic.alarms.arn]

  tags = {
    Project = var.project_name
  }
}

# 3. ECS — High memory (>90% for 5 min)
resource "aws_cloudwatch_metric_alarm" "ecs_high_memory" {
  alarm_name          = "${lower(var.project_name)}-ecs-high-memory"
  alarm_description   = "WARNING: ECS memory utilization above 90%"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "MemoryUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 90

  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = aws_ecs_service.api.name
  }

  alarm_actions = [aws_sns_topic.alarms.arn]
  ok_actions    = [aws_sns_topic.alarms.arn]

  tags = {
    Project = var.project_name
  }
}

# 4. API Gateway — 5xx server errors (backend failures)
resource "aws_cloudwatch_metric_alarm" "apigw_5xx_errors" {
  alarm_name          = "${lower(var.project_name)}-apigw-5xx-errors"
  alarm_description   = "CRITICAL: API returning 5xx errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "5xx"
  namespace           = "AWS/ApiGateway"
  period              = 300
  statistic           = "Sum"
  threshold           = 10

  dimensions = {
    ApiId = aws_apigatewayv2_api.api.id
  }

  alarm_actions = [aws_sns_topic.alarms.arn]
  ok_actions    = [aws_sns_topic.alarms.arn]

  tags = {
    Project = var.project_name
  }
}

# 5. API Gateway — High latency (p95 > 5 seconds)
resource "aws_cloudwatch_metric_alarm" "apigw_high_latency" {
  alarm_name          = "${lower(var.project_name)}-apigw-high-latency"
  alarm_description   = "WARNING: API p95 latency exceeds 5 seconds"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Latency"
  namespace           = "AWS/ApiGateway"
  period              = 300
  extended_statistic  = "p95"
  threshold           = 5000

  dimensions = {
    ApiId = aws_apigatewayv2_api.api.id
  }

  alarm_actions = [aws_sns_topic.alarms.arn]
  ok_actions    = [aws_sns_topic.alarms.arn]

  tags = {
    Project = var.project_name
  }
}
