#!/bin/bash
# Deployment Script for S3 Log Retention Infrastructure
# Usage: ./deploy.sh <environment> [options]

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_usage() {
    cat << EOF
Usage: $0 <environment> [options]

Environments:
  dev       - Development environment
  staging   - Staging environment
  prod      - Production environment

Options:
  --auto-approve    Skip confirmation prompts
  --destroy         Destroy infrastructure instead of creating
  --plan-only       Only run terraform plan
  --help            Show this help message

Examples:
  $0 dev                    # Deploy to dev environment
  $0 prod --plan-only       # Plan production deployment
  $0 staging --auto-approve # Deploy to staging without prompts

EOF
}

# Parse arguments
ENVIRONMENT=""
AUTO_APPROVE=""
DESTROY=false
PLAN_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        dev|staging|prod)
            ENVIRONMENT=$1
            shift
            ;;
        --auto-approve)
            AUTO_APPROVE="-auto-approve"
            shift
            ;;
        --destroy)
            DESTROY=true
            shift
            ;;
        --plan-only)
            PLAN_ONLY=true
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate environment
if [[ -z "$ENVIRONMENT" ]]; then
    log_error "Environment not specified"
    show_usage
    exit 1
fi

# Terraform directory
TF_DIR="$PROJECT_ROOT/terraform"
TF_VARS_FILE="$TF_DIR/environments/$ENVIRONMENT/terraform.tfvars"

# Validate terraform vars file exists
if [[ ! -f "$TF_VARS_FILE" ]]; then
    log_error "Terraform vars file not found: $TF_VARS_FILE"
    exit 1
fi

log_info "Starting deployment for environment: $ENVIRONMENT"

# Navigate to terraform directory
cd "$TF_DIR"

# Initialize Terraform
log_info "Initializing Terraform..."
terraform init -upgrade

# Validate configuration
log_info "Validating Terraform configuration..."
terraform validate

if [[ $? -ne 0 ]]; then
    log_error "Terraform validation failed"
    exit 1
fi

# Format check
log_info "Checking Terraform formatting..."
terraform fmt -check -recursive || {
    log_warn "Terraform files are not formatted. Run 'terraform fmt -recursive' to fix."
}

# Plan
log_info "Running Terraform plan..."
terraform plan -var-file="$TF_VARS_FILE" -out=tfplan

if [[ $PLAN_ONLY == true ]]; then
    log_info "Plan-only mode. Exiting."
    exit 0
fi

# Apply or Destroy
if [[ $DESTROY == true ]]; then
    log_warn "DESTROY mode enabled. This will remove all infrastructure."
    if [[ -z "$AUTO_APPROVE" ]]; then
        read -p "Are you sure you want to destroy $ENVIRONMENT? (yes/no): " confirm
        if [[ "$confirm" != "yes" ]]; then
            log_info "Deployment cancelled"
            exit 0
        fi
        AUTO_APPROVE="-auto-approve"
    fi
    
    log_info "Destroying infrastructure..."
    terraform destroy -var-file="$TF_VARS_FILE" $AUTO_APPROVE
else
    log_info "Applying Terraform plan..."
    terraform apply $AUTO_APPROVE tfplan
fi

# Cleanup plan file
rm -f tfplan

# Output results
if [[ $DESTROY == true ]]; then
    log_info "Infrastructure destroyed successfully"
else
    log_info "Deployment completed successfully"
    log_info "Terraform outputs:"
    terraform output
fi

# Run post-deployment validation
if [[ $DESTROY == false ]]; then
    log_info "Running post-deployment validation..."
    "$SCRIPT_DIR/../validate/validate-deployment.sh" "$ENVIRONMENT"
fi

log_info "Done!"
