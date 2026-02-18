# ── Security Groups ──

# ALB — accepts HTTP/HTTPS from the internet
resource "aws_security_group" "alb" {
  name        = "${lower(var.project_name)}-alb-sg"
  description = "Allow HTTP/HTTPS inbound to ALB"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${lower(var.project_name)}-alb-sg"
    Project = var.project_name
  }
}

# ECS Tasks — only accepts traffic from ALB
resource "aws_security_group" "ecs" {
  name        = "${lower(var.project_name)}-ecs-sg"
  description = "Allow inbound from ALB only"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description     = "From ALB"
    from_port       = var.api_container_port
    to_port         = var.api_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "All outbound (MongoDB Atlas, Razorpay, Resend, etc.)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${lower(var.project_name)}-ecs-sg"
    Project = var.project_name
  }
}
