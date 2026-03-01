variable "aws_profile" {
  description = "AWS CLI profile to use"
  type        = string
  default     = "nandishdave-personal-1"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name used for tagging"
  type        = string
  default     = "VedicJivan"
}

variable "hosted_zone_name" {
  description = "Route 53 hosted zone name"
  type        = string
  default     = "nandishdave.world"
}

variable "acm_certificate_arn" {
  description = "ARN of existing ACM certificate for frontend CloudFront (us-east-1). Leave empty to create one via Terraform."
  type        = string
  default     = ""
}

# ── Backend Infrastructure ──

variable "api_container_port" {
  description = "Port the FastAPI container listens on"
  type        = number
  default     = 8000
}

variable "api_cpu" {
  description = "Fargate task CPU units (256 = 0.25 vCPU)"
  type        = number
  default     = 256
}

variable "api_memory" {
  description = "Fargate task memory in MiB"
  type        = number
  default     = 512
}

variable "api_desired_count" {
  description = "Number of running API tasks"
  type        = number
  default     = 1
}

variable "alarm_email" {
  description = "Email address for CloudWatch alarm notifications"
  type        = string
  default     = "vedic.jivan33@gmail.com"
}

# ── Test Environment Protection ──

variable "test_site_username" {
  description = "Basic auth username for test environment (leave empty to disable)"
  type        = string
  default     = ""
}

variable "test_site_password" {
  description = "Basic auth password for test environment (leave empty to disable)"
  type        = string
  default     = ""
  sensitive   = true
}
