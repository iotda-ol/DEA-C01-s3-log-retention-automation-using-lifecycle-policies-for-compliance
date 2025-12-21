#!/bin/bash
# Deployment Script for S3 Log Retention Automation
# This script automates the deployment of the infrastructure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
EXAMPLE_DIR="${1:-basic}"
TERRAFORM_DIR="examples/${EXAMPLE_DIR}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}S3 Log Retention Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v terraform &> /dev/null; then
    echo -e "${RED}Error: Terraform is not installed${NC}"
    exit 1
fi

if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is not installed${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites installed${NC}"
echo ""

# Verify AWS credentials
echo -e "${YELLOW}Verifying AWS credentials...${NC}"
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}Error: AWS credentials not configured${NC}"
    exit 1
fi

AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region || echo "us-east-1")

echo -e "${GREEN}✓ AWS Account: ${AWS_ACCOUNT}${NC}"
echo -e "${GREEN}✓ AWS Region: ${AWS_REGION}${NC}"
echo ""

# Check if terraform directory exists
if [ ! -d "$TERRAFORM_DIR" ]; then
    echo -e "${RED}Error: Directory ${TERRAFORM_DIR} not found${NC}"
    exit 1
fi

cd "$TERRAFORM_DIR"

# Check for terraform.tfvars
if [ ! -f "terraform.tfvars" ]; then
    echo -e "${YELLOW}Warning: terraform.tfvars not found${NC}"
    if [ -f "terraform.tfvars.example" ]; then
        echo -e "${YELLOW}Creating terraform.tfvars from example...${NC}"
        cp terraform.tfvars.example terraform.tfvars
        echo -e "${RED}Please edit terraform.tfvars with your configuration${NC}"
        exit 1
    fi
fi

# Initialize Terraform
echo -e "${YELLOW}Initializing Terraform...${NC}"
terraform init

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Terraform initialization failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Terraform initialized${NC}"
echo ""

# Validate Terraform configuration
echo -e "${YELLOW}Validating Terraform configuration...${NC}"
terraform validate

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Terraform validation failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuration valid${NC}"
echo ""

# Plan deployment
echo -e "${YELLOW}Planning deployment...${NC}"
terraform plan -out=tfplan

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Terraform plan failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Plan created${NC}"
echo ""

# Ask for confirmation
read -p "Do you want to apply this plan? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Deployment cancelled${NC}"
    exit 0
fi

# Apply deployment
echo -e "${YELLOW}Applying deployment...${NC}"
terraform apply tfplan

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Terraform apply failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Display outputs
echo -e "${YELLOW}Deployment Outputs:${NC}"
terraform output

echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "1. Verify bucket creation: aws s3 ls"
echo "2. Check lifecycle policy: aws s3api get-bucket-lifecycle-configuration --bucket <bucket-name>"
echo "3. Test with Python CLI: python3 -m python.src.cli.main list-buckets"
echo ""
