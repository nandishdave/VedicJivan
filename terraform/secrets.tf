# ── SSM Parameter Store ──
# Stores sensitive environment variables for the ECS task (free tier).
# After terraform apply, populate each parameter via AWS CLI:
#
#   aws ssm put-parameter --name "/vedicjivan/MONGODB_URI" --value "mongodb+srv://..." --type SecureString --overwrite --profile nandishdave-personal-1
#   aws ssm put-parameter --name "/vedicjivan/JWT_SECRET" --value "..." --type SecureString --overwrite --profile nandishdave-personal-1
#   aws ssm put-parameter --name "/vedicjivan/RAZORPAY_KEY_ID" --value "..." --type SecureString --overwrite --profile nandishdave-personal-1
#   aws ssm put-parameter --name "/vedicjivan/RAZORPAY_KEY_SECRET" --value "..." --type SecureString --overwrite --profile nandishdave-personal-1
#   aws ssm put-parameter --name "/vedicjivan/RAZORPAY_WEBHOOK_SECRET" --value "" --type SecureString --overwrite --profile nandishdave-personal-1
#   aws ssm put-parameter --name "/vedicjivan/RESEND_API_KEY" --value "" --type SecureString --overwrite --profile nandishdave-personal-1
#   aws ssm put-parameter --name "/vedicjivan/ADMIN_EMAIL" --value "vedic.jivan33@gmail.com" --type SecureString --overwrite --profile nandishdave-personal-1

locals {
  ssm_prefix = "/${lower(var.project_name)}"
  secret_params = [
    "MONGODB_URI",
    "JWT_SECRET",
    "RAZORPAY_KEY_ID",
    "RAZORPAY_KEY_SECRET",
    "RAZORPAY_WEBHOOK_SECRET",
    "RESEND_API_KEY",
    "ADMIN_EMAIL",
  ]
}

# Create placeholder parameters — values populated via AWS CLI after apply
resource "aws_ssm_parameter" "api_secrets" {
  for_each = toset(local.secret_params)

  name  = "${local.ssm_prefix}/${each.value}"
  type  = "SecureString"
  value = "PLACEHOLDER" # Overwrite via AWS CLI after apply

  tags = {
    Project = var.project_name
  }

  lifecycle {
    ignore_changes = [value] # Don't overwrite manually set values
  }
}
