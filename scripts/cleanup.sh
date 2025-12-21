#!/bin/bash
# Cleanup Script for S3 Log Retention
# Destroys infrastructure created by Terraform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

EXAMPLE_DIR="${1:-basic}"
TERRAFORM_DIR="examples/${EXAMPLE_DIR}"

echo -e "${RED}========================================${NC}"
echo -e "${RED}S3 Log Retention Cleanup Script${NC}"
echo -e "${RED}========================================${NC}"
echo ""
echo -e "${RED}WARNING: This will destroy all resources!${NC}"
echo ""

# Check if terraform directory exists
if [ ! -d "$TERRAFORM_DIR" ]; then
    echo -e "${RED}Error: Directory ${TERRAFORM_DIR} not found${NC}"
    exit 1
fi

cd "$TERRAFORM_DIR"

# Show what will be destroyed
echo -e "${YELLOW}Resources to be destroyed:${NC}"
terraform show

echo ""
read -p "Are you sure you want to destroy all resources? Type 'yes' to confirm: " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Cleanup cancelled${NC}"
    exit 0
fi

# Get bucket name before destroying
BUCKET_NAME=$(terraform output -raw bucket_id 2>/dev/null || echo "")

if [ -n "$BUCKET_NAME" ]; then
    echo -e "${YELLOW}Checking if bucket needs to be emptied...${NC}"

    # Check if bucket has objects
    OBJECT_COUNT=$(aws s3api list-objects-v2 --bucket "$BUCKET_NAME" --query 'length(Contents)' --output text 2>/dev/null || echo "0")

    if [ "$OBJECT_COUNT" != "0" ] && [ "$OBJECT_COUNT" != "None" ]; then
        echo -e "${YELLOW}Bucket has ${OBJECT_COUNT} objects${NC}"
        read -p "Do you want to empty the bucket? (yes/no): " EMPTY_CONFIRM

        if [ "$EMPTY_CONFIRM" == "yes" ]; then
            echo -e "${YELLOW}Emptying bucket...${NC}"
            aws s3 rm "s3://${BUCKET_NAME}" --recursive

            # Also delete versioned objects if versioning is enabled
            echo -e "${YELLOW}Deleting versioned objects...${NC}"
            aws s3api delete-objects --bucket "$BUCKET_NAME" \
                --delete "$(aws s3api list-object-versions --bucket "$BUCKET_NAME" \
                --query '{Objects: Versions[].{Key: Key, VersionId: VersionId}}' \
                --output json)" 2>/dev/null || true

            echo -e "${GREEN}✓ Bucket emptied${NC}"
        fi
    fi
fi

# Destroy infrastructure
echo -e "${YELLOW}Destroying infrastructure...${NC}"
terraform destroy -auto-approve

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Terraform destroy failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Cleanup completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
