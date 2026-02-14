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
  description = "ARN of the ACM certificate (must be in us-east-1)"
  type        = string
  default     = "arn:aws:acm:us-east-1:478821518696:certificate/785e6d27-7c86-4246-9e20-26af8bfdf18d"
}
