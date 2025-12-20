#!/bin/bash
# Quick setup script for development environment

set -e

echo "S3 Log Retention Automation - Quick Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Check AWS CLI
echo "Checking AWS CLI..."
aws --version

# Check Terraform
echo "Checking Terraform..."
terraform --version

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
cd python
pip install -r requirements.txt
pip install -r requirements-dev.txt
cd ..

# Initialize Terraform
echo ""
echo "Initializing Terraform..."
cd terraform/environments/dev
terraform init
terraform validate
cd ../../..

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Configure AWS credentials: aws configure"
echo "  2. Review Terraform config: terraform/environments/dev/"
echo "  3. Run Python CLI: python python/main.py --help"
