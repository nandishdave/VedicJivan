# ── ECS Cluster ──

resource "aws_ecs_cluster" "main" {
  name = "${lower(var.project_name)}-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled" # Enable later if needed (adds cost)
  }

  tags = {
    Project = var.project_name
  }
}

# ── Task Definition ──

resource "aws_ecs_task_definition" "api" {
  family                   = "${lower(var.project_name)}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.api_cpu
  memory                   = var.api_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name      = "${lower(var.project_name)}-api"
      image     = "${aws_ecr_repository.api.repository_url}:latest"
      essential = true

      portMappings = [
        {
          containerPort = var.api_container_port
          hostPort      = var.api_container_port
          protocol      = "tcp"
        }
      ]

      # Non-sensitive environment variables
      environment = [
        { name = "APP_ENV", value = "production" },
        { name = "APP_URL", value = "https://${var.api_domain_name}" },
        { name = "FRONTEND_URL", value = "https://${var.domain_name}" },
        { name = "EMAIL_FROM", value = "noreply@vedicjivan.com" },
        { name = "JWT_ALGORITHM", value = "HS256" },
        { name = "ACCESS_TOKEN_EXPIRE_MINUTES", value = "15" },
        { name = "REFRESH_TOKEN_EXPIRE_DAYS", value = "7" },
      ]

      # Sensitive values from SSM Parameter Store (free tier)
      secrets = [
        for param in local.secret_params : {
          name      = param
          valueFrom = aws_ssm_parameter.api_secrets[param].arn
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.api.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }

      # Health check at container level
      healthCheck = {
        command     = ["CMD-SHELL", "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:${var.api_container_port}/api/health')\" || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])

  tags = {
    Project = var.project_name
  }
}

# ── ECS Service ──

resource "aws_ecs_service" "api" {
  name            = "${lower(var.project_name)}-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.api_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true # Required for Fargate in public subnets (to pull ECR images and reach internet)
  }

  # Service discovery registration (for API Gateway VPC Link)
  service_registries {
    registry_arn   = aws_service_discovery_service.api.arn
    container_name = "${lower(var.project_name)}-api"
    container_port = var.api_container_port
  }

  # Allow ECS to manage task placement during deployments
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  # Ignore desired_count changes from auto-scaling or manual console changes
  lifecycle {
    ignore_changes = [desired_count]
  }

  tags = {
    Project = var.project_name
  }
}
