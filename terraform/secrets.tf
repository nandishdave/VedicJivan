# ── SSM Parameter Store ──
# Stores sensitive environment variables for the ECS task (free tier).
# After terraform apply, populate each parameter via AWS CLI:
#
#   MSYS_NO_PATHCONV=1 aws ssm put-parameter --name "<prefix>/MONGODB_URI" --value "mongodb+srv://..." --type SecureString --overwrite --region ap-south-1 --profile nandishdave-personal-1
#
# Where <prefix> is the ssm_parameter_prefix output (e.g. /vedicjivan or /vedicjivan-test)

# Create placeholder parameters — values populated via AWS CLI after apply
resource "aws_ssm_parameter" "api_secrets" {
  for_each = toset(local.secret_params)

  name  = "${local.ssm_prefix}/${each.value}"
  type  = "SecureString"
  value = "PLACEHOLDER" # Overwrite via AWS CLI after apply

  tags = local.common_tags

  lifecycle {
    ignore_changes = [value] # Don't overwrite manually set values
  }
}
