#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════
#  VedicJivan Environment Toggle
# ═══════════════════════════════════════════════════════
#  Usage:  ./switch-env.sh prod    — activate prod, shut down test
#          ./switch-env.sh test    — activate test, shut down prod
#
#  What it does:
#   1. Puts the INACTIVE environment into maintenance mode
#      (CloudFront returns 503 page, ECS scales to 0 tasks)
#   2. Takes the ACTIVE environment out of maintenance mode
#      (CloudFront serves normally, ECS scales back up)
# ═══════════════════════════════════════════════════════

set -euo pipefail

TARGET="${1:-}"

if [[ "$TARGET" != "prod" && "$TARGET" != "test" ]]; then
  echo "Usage: $0 <prod|test>"
  echo ""
  echo "  prod  — activate production, shut down test"
  echo "  test  — activate test, shut down production"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "═══════════════════════════════════════════════"
echo "  Switching active environment to: $TARGET"
echo "═══════════════════════════════════════════════"
echo ""

if [[ "$TARGET" == "prod" ]]; then
  # Step 1: Shut down test environment
  echo "▸ Step 1/2: Shutting down TEST environment..."
  echo "  (workspace: test, maintenance_mode = true)"
  echo ""
  terraform workspace select test
  terraform apply -var-file=test.tfvars -var "maintenance_mode=true" -auto-approve
  echo ""
  echo "  ✓ Test environment shut down."
  echo ""

  # Step 2: Activate prod environment
  echo "▸ Step 2/2: Activating PROD environment..."
  echo "  (workspace: default, maintenance_mode = false)"
  echo ""
  terraform workspace select default
  terraform apply -var-file=prod.tfvars -var "maintenance_mode=false" -auto-approve
  echo ""
  echo "  ✓ Production environment activated."

else
  # Step 1: Shut down prod environment
  echo "▸ Step 1/2: Shutting down PROD environment..."
  echo "  (workspace: default, maintenance_mode = true)"
  echo ""
  terraform workspace select default
  terraform apply -var-file=prod.tfvars -var "maintenance_mode=true" -auto-approve
  echo ""
  echo "  ✓ Production environment shut down."
  echo ""

  # Step 2: Activate test environment
  echo "▸ Step 2/2: Activating TEST environment..."
  echo "  (workspace: test, maintenance_mode = false)"
  echo ""
  terraform workspace select test
  terraform apply -var-file=test.tfvars -var "maintenance_mode=false" -auto-approve
  echo ""
  echo "  ✓ Test environment activated."
fi

echo ""
echo "═══════════════════════════════════════════════"
echo "  Done! Active environment: $TARGET"
echo "═══════════════════════════════════════════════"
echo ""
echo "  Current terraform workspace: $(terraform workspace show)"
echo ""
