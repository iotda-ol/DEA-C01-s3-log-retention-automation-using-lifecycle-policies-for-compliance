# Quick Start Guide

## Overview

This guide will help you quickly deploy the S3 log retention automation solution.

## Prerequisites

Before you begin, ensure you have:
- AWS account with appropriate permissions
- AWS CLI configured with credentials
- Terraform >= 1.0 installed
- Python 3.8+ installed

## 5-Minute Quick Start

### Step 1: Clone Repository

```bash
git clone https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance
```

### Step 2: Install Python Dependencies

```bash
pip install -r python/requirements.txt
```

### Step 3: Configure Deployment

```bash
cd examples/basic
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your bucket name
```

### Step 4: Deploy Infrastructure

```bash
# Using the deployment script
../../scripts/deploy.sh basic

# Or manually
terraform init
terraform plan
terraform apply
```

### Step 5: Verify Deployment

```bash
# Using the validation script
../../scripts/validate.sh <your-bucket-name>

# Or using Python CLI
cd ../..
python3 -m python.src.cli.main list-buckets
python3 -m python.src.cli.main bucket-info <your-bucket-name>
```

## What Gets Deployed

The basic deployment creates:

1. **S3 Bucket** with:
   - Server-side encryption (AES256)
   - Versioning enabled
   - Public access blocked
   - Tags for compliance

2. **Lifecycle Policy** with:
   - Transition to Standard-IA after 30 days
   - Transition to Glacier after 90 days
   - Automatic deletion after 365 days (compliance requirement)

3. **IAM Roles** (optional):
   - Lambda execution role for automation

4. **CloudWatch Monitoring**:
   - Dashboard for bucket metrics
   - Alarms for size and error thresholds

## Testing the Solution

### Upload Test Logs

```bash
# Create a test log file
echo "Test log entry" > test.log

# Upload to bucket
aws s3 cp test.log s3://<your-bucket-name>/logs/2024/01/01/test.log
```

### Verify Lifecycle Policy

```bash
# Check lifecycle configuration
aws s3api get-bucket-lifecycle-configuration --bucket <your-bucket-name>

# Or use Python CLI
python3 -m python.src.cli.main validate-policy <your-bucket-name>
```

### Generate Compliance Report

```bash
python3 -m python.src.cli.main compliance-report <your-bucket-name>

# Save to file
python3 -m python.src.cli.main compliance-report <your-bucket-name> \
  --format json --output report.json
```

## Common Configurations

### Change Retention Period

Edit `terraform.tfvars`:
```hcl
retention_days = 730  # 2 years instead of 1
```

### Enable KMS Encryption

```hcl
encryption_type = "aws:kms"
kms_key_id = "arn:aws:kms:region:account:key/key-id"
```

### Disable Monitoring

```hcl
enable_monitoring = false
```

## Cleanup

To destroy all resources:

```bash
# Using the cleanup script
./scripts/cleanup.sh basic

# Or manually
cd examples/basic
terraform destroy
```

## Next Steps

- Read the [100-Step Manual](MANUAL.md) for comprehensive learning
- Review [Architecture Documentation](docs/ARCHITECTURE.md)
- Explore [Advanced Examples](examples/advanced/)
- Set up [CI/CD Pipeline](.github/workflows/)

## Troubleshooting

### Error: Bucket Already Exists

Bucket names must be globally unique. Change the `bucket_name` in `terraform.tfvars`.

### Error: AWS Credentials Not Found

Configure AWS CLI:
```bash
aws configure
```

### Error: Terraform Not Found

Install Terraform:
```bash
# macOS
brew install terraform

# Linux
# Follow instructions at terraform.io
```

## Support

- GitHub Issues: Report bugs or request features
- Documentation: See `/docs` folder
- Examples: See `/examples` folder
