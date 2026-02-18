# ── API Gateway HTTP API (replaces ALB — $0 base cost vs $16/month) ──

resource "aws_apigatewayv2_api" "api" {
  name          = "${lower(var.project_name)}-api"
  protocol_type = "HTTP"

  tags = {
    Project = var.project_name
  }
}

# VPC Link — connects API Gateway to ECS tasks in the VPC (free for HTTP APIs)
resource "aws_apigatewayv2_vpc_link" "api" {
  name               = "${lower(var.project_name)}-vpc-link"
  security_group_ids = [aws_security_group.ecs.id]
  subnet_ids         = data.aws_subnets.default.ids

  tags = {
    Project = var.project_name
  }
}

# Integration — routes traffic to ECS via Cloud Map service discovery
resource "aws_apigatewayv2_integration" "api" {
  api_id             = aws_apigatewayv2_api.api.id
  integration_type   = "HTTP_PROXY"
  integration_method = "ANY"
  integration_uri    = aws_service_discovery_service.api.arn
  connection_type    = "VPC_LINK"
  connection_id      = aws_apigatewayv2_vpc_link.api.id
}

# Default route — forward all requests to the ECS integration
resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}

# Auto-deploy stage with access logging
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      path           = "$context.path"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
      latency        = "$context.integrationLatency"
      errorMessage   = "$context.error.message"
    })
  }

  tags = {
    Project = var.project_name
  }
}

# Custom domain for API Gateway
resource "aws_apigatewayv2_domain_name" "api" {
  domain_name = var.api_domain_name

  domain_name_configuration {
    certificate_arn = aws_acm_certificate_validation.api.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  tags = {
    Project = var.project_name
  }
}

# Map custom domain to the API
resource "aws_apigatewayv2_api_mapping" "api" {
  api_id      = aws_apigatewayv2_api.api.id
  domain_name = aws_apigatewayv2_domain_name.api.id
  stage       = aws_apigatewayv2_stage.default.id
}

# ── Cloud Map (Service Discovery) ──
# API Gateway VPC Link uses Cloud Map to find ECS tasks

resource "aws_service_discovery_private_dns_namespace" "main" {
  name = "${lower(var.project_name)}.local"
  vpc  = data.aws_vpc.default.id

  tags = {
    Project = var.project_name
  }
}

resource "aws_service_discovery_service" "api" {
  name = "api"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.main.id

    dns_records {
      type = "SRV"
      ttl  = 10
    }
  }

  health_check_custom_config {
    failure_threshold = 1
  }

  tags = {
    Project = var.project_name
  }
}
