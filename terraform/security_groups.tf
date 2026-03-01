# ── Security Groups ──

# ECS Tasks — allows traffic from API Gateway VPC Link + outbound for external services
resource "aws_security_group" "ecs" {
  name        = "${local.name_prefix}-ecs-sg"
  description = "Allow inbound from API Gateway VPC Link"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "From API Gateway VPC Link"
    from_port   = var.api_container_port
    to_port     = var.api_container_port
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.default.cidr_block] # VPC Link originates from within the VPC
  }

  egress {
    description = "All outbound (MongoDB Atlas, Stripe, Resend, etc.)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${local.name_prefix}-ecs-sg"
    Project     = var.project_name
    Environment = local.env
  }
}
