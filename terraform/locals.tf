# ── Workspace-aware naming ──
# "default" workspace = prod, "test" workspace = test environment

locals {
  # Environment name derived from workspace
  env = terraform.workspace == "default" ? "prod" : terraform.workspace

  # Resource name prefix: "vedicjivan" for prod, "vedicjivan-test" for test
  name_prefix = terraform.workspace == "default" ? lower(var.project_name) : "${lower(var.project_name)}-${local.env}"

  # Domain names
  frontend_domain = terraform.workspace == "default" ? "vedicjivan.${var.hosted_zone_name}" : "${lower(var.project_name)}-${local.env}.${var.hosted_zone_name}"
  api_domain      = terraform.workspace == "default" ? "api.vedicjivan.${var.hosted_zone_name}" : "api.${lower(var.project_name)}-${local.env}.${var.hosted_zone_name}"

  # SSM parameter prefix: "/vedicjivan" for prod, "/vedicjivan-test" for test
  ssm_prefix = "/${local.name_prefix}"

  # Common tags for all resources
  common_tags = {
    Project     = var.project_name
    Environment = local.env
  }

  # Secret parameter names (used by secrets.tf and iam.tf)
  secret_params = [
    "MONGODB_URI",
    "JWT_SECRET",
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET",
    "RESEND_API_KEY",
    "ADMIN_EMAIL",
    "INTERNAL_SECRET",
  ]
}
