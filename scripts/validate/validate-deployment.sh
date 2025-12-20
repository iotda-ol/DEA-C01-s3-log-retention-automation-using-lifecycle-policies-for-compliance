#!/bin/bash
# Validation Script for Deployment
# Usage: ./validate-deployment.sh <environment>

set -e

ENVIRONMENT=$1
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [[ -z "$ENVIRONMENT" ]]; then
    echo "Usage: $0 <environment>"
    exit 1
fi

echo "=== Validating Deployment for $ENVIRONMENT ==="

# Get Terraform outputs
cd "$PROJECT_ROOT/terraform"
BUCKET_NAME=$(terraform output -raw log_bucket_id 2>/dev/null || echo "")

if [[ -z "$BUCKET_NAME" ]]; then
    echo "ERROR: Could not get bucket name from Terraform outputs"
    exit 1
fi

echo "✓ Bucket name: $BUCKET_NAME"

# Check bucket exists
echo "Checking bucket existence..."
if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
    echo "✓ Bucket exists"
else
    echo "✗ Bucket does not exist"
    exit 1
fi

# Check versioning
echo "Checking versioning..."
VERSIONING=$(aws s3api get-bucket-versioning --bucket "$BUCKET_NAME" --query 'Status' --output text 2>/dev/null || echo "")
if [[ "$VERSIONING" == "Enabled" ]]; then
    echo "✓ Versioning enabled"
else
    echo "✗ Versioning not enabled"
    exit 1
fi

# Check encryption
echo "Checking encryption..."
ENCRYPTION=$(aws s3api get-bucket-encryption --bucket "$BUCKET_NAME" 2>/dev/null && echo "enabled" || echo "disabled")
if [[ "$ENCRYPTION" == "enabled" ]]; then
    echo "✓ Encryption enabled"
else
    echo "✗ Encryption not enabled"
    exit 1
fi

# Check lifecycle policy
echo "Checking lifecycle policy..."
LIFECYCLE=$(aws s3api get-bucket-lifecycle-configuration --bucket "$BUCKET_NAME" 2>/dev/null && echo "configured" || echo "not-configured")
if [[ "$LIFECYCLE" == "configured" ]]; then
    echo "✓ Lifecycle policy configured"
else
    echo "✗ Lifecycle policy not configured"
    exit 1
fi

# Check public access block
echo "Checking public access block..."
PUBLIC_BLOCK=$(aws s3api get-public-access-block --bucket "$BUCKET_NAME" 2>/dev/null && echo "configured" || echo "not-configured")
if [[ "$PUBLIC_BLOCK" == "configured" ]]; then
    echo "✓ Public access blocked"
else
    echo "✗ Public access not blocked"
    exit 1
fi

echo ""
echo "=== All Validation Checks Passed ==="
echo ""
