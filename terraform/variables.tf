variable "aws_profile" {
  description = "AWS CLI profile to use"
  type        = string
  default     = "nandishdave-personal-1"
}

variable "aws_region" {
  description = "AWS region for S3 bucket"
  type        = string
  default     = "ap-south-1"
}

variable "bucket_name" {
  description = "S3 bucket name for the static website"
  type        = string
  default     = "vedicjivan-website"
}

variable "project_name" {
  description = "Project name used for tagging"
  type        = string
  default     = "VedicJivan"
}

variable "domain_name" {
  description = "Custom domain name for the website"
  type        = string
  default     = "vedicjivan.nandishdave.world"
}

variable "acm_certificate_arn" {
  description = "ARN of the ACM certificate for frontend (must be in us-east-1 for CloudFront)"
  type        = string
  default     = "arn:aws:acm:us-east-1:478821518696:certificate/785e6d27-7c86-4246-9e20-26af8bfdf18d"
}

# ── Backend Infrastructure ──

variable "api_domain_name" {
  description = "Custom domain for the API (ALB)"
  type        = string
  default     = "api.vedicjivan.nandishdave.world"
}

variable "hosted_zone_name" {
  description = "Route 53 hosted zone name"
  type        = string
  default     = "nandishdave.world"
}

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
