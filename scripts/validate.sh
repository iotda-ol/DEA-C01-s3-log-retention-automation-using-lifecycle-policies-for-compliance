#!/bin/bash
# Validation Script for S3 Log Retention
# Validates deployed infrastructure and compliance

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BUCKET_NAME="$1"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}S3 Log Retention Validation Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

if [ -z "$BUCKET_NAME" ]; then
    echo -e "${RED}Error: Bucket name required${NC}"
    echo "Usage: $0 <bucket-name>"
    exit 1
fi

# Check if bucket exists
echo -e "${YELLOW}Checking if bucket exists...${NC}"
if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
    echo -e "${GREEN}✓ Bucket exists${NC}"
else
    echo -e "${RED}✗ Bucket does not exist${NC}"
    exit 1
fi

# Check bucket encryption
echo -e "${YELLOW}Checking bucket encryption...${NC}"
if aws s3api get-bucket-encryption --bucket "$BUCKET_NAME" &>/dev/null; then
    echo -e "${GREEN}✓ Bucket encryption enabled${NC}"
    aws s3api get-bucket-encryption --bucket "$BUCKET_NAME" --query 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm' --output text
else
    echo -e "${RED}✗ Bucket encryption not configured${NC}"
fi

# Check versioning
echo -e "${YELLOW}Checking bucket versioning...${NC}"
VERSIONING=$(aws s3api get-bucket-versioning --bucket "$BUCKET_NAME" --query 'Status' --output text)
if [ "$VERSIONING" == "Enabled" ]; then
    echo -e "${GREEN}✓ Versioning enabled${NC}"
else
    echo -e "${YELLOW}⚠ Versioning not enabled${NC}"
fi

# Check public access block
echo -e "${YELLOW}Checking public access block...${NC}"
if aws s3api get-public-access-block --bucket "$BUCKET_NAME" &>/dev/null; then
    echo -e "${GREEN}✓ Public access block configured${NC}"
    aws s3api get-public-access-block --bucket "$BUCKET_NAME"
else
    echo -e "${RED}✗ Public access block not configured${NC}"
fi

# Check lifecycle configuration
echo -e "${YELLOW}Checking lifecycle configuration...${NC}"
if aws s3api get-bucket-lifecycle-configuration --bucket "$BUCKET_NAME" &>/dev/null; then
    echo -e "${GREEN}✓ Lifecycle policy configured${NC}"

    # Get expiration days
    EXPIRATION_DAYS=$(aws s3api get-bucket-lifecycle-configuration --bucket "$BUCKET_NAME" --query 'Rules[0].Expiration.Days' --output text 2>/dev/null || echo "N/A")

    if [ "$EXPIRATION_DAYS" != "N/A" ]; then
        echo -e "${GREEN}  Retention period: ${EXPIRATION_DAYS} days${NC}"

        if [ "$EXPIRATION_DAYS" -ge 365 ]; then
            echo -e "${GREEN}  ✓ Meets compliance requirement (365 days)${NC}"
        else
            echo -e "${RED}  ✗ Does not meet compliance requirement${NC}"
        fi
    fi
else
    echo -e "${RED}✗ Lifecycle policy not configured${NC}"
fi

# Check bucket tags
echo -e "${YELLOW}Checking bucket tags...${NC}"
if aws s3api get-bucket-tagging --bucket "$BUCKET_NAME" &>/dev/null; then
    echo -e "${GREEN}✓ Bucket tags configured${NC}"
    aws s3api get-bucket-tagging --bucket "$BUCKET_NAME" --query 'TagSet[*].[Key,Value]' --output table
else
    echo -e "${YELLOW}⚠ No bucket tags${NC}"
fi

# Get bucket size and object count
echo -e "${YELLOW}Getting bucket statistics...${NC}"
OBJECT_COUNT=$(aws s3api list-objects-v2 --bucket "$BUCKET_NAME" --query 'length(Contents)' --output text 2>/dev/null || echo "0")
echo -e "${GREEN}  Objects: ${OBJECT_COUNT}${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Validation completed${NC}"
echo -e "${GREEN}========================================${NC}"
