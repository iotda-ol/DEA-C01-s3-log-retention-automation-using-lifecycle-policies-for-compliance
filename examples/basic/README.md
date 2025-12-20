# Basic S3 Log Retention Example

This example demonstrates a simple S3 log retention setup with lifecycle policies.

## Overview

- Single S3 bucket for application logs
- 365-day retention policy (DEA-C01 compliant)
- Automatic transitions to cheaper storage classes
- CloudWatch monitoring

## Prerequisites

- AWS account configured
- Terraform installed
- AWS CLI configured

## Quick Start

```bash
# 1. Navigate to example directory
cd examples/basic

# 2. Initialize Terraform
terraform init

# 3. Review the plan
terraform plan

# 4. Apply configuration
terraform apply

# 5. Verify deployment
aws s3 ls | grep log-retention
```

## What Gets Created

1. **S3 Bucket**: `basic-log-retention-{account-id}`
   - Versioning enabled
   - AES256 encryption
   - Public access blocked

2. **Lifecycle Policy**:
   - Day 0-30: STANDARD storage
   - Day 30-90: STANDARD_IA storage
   - Day 90-180: GLACIER storage
   - Day 180-365: DEEP_ARCHIVE storage
   - Day 365+: Automatic deletion

3. **CloudWatch Alarm**: Storage quota monitoring

## Configuration

**main.tf**:
```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Use the reusable modules from parent directory
module "log_bucket" {
  source = "../../terraform/modules/s3-bucket"

  bucket_name       = "basic-log-retention-${data.aws_caller_identity.current.account_id}"
  enable_versioning = true
  
  tags = {
    Example     = "basic"
    Environment = "demo"
  }
}

module "lifecycle_policy" {
  source    = "../../terraform/modules/lifecycle-policy"
  bucket_id = module.log_bucket.bucket_id

  lifecycle_rules = [
    {
      id      = "basic-retention"
      enabled = true
      transitions = [
        { days = 30, storage_class = "STANDARD_IA" },
        { days = 90, storage_class = "GLACIER" },
        { days = 180, storage_class = "DEEP_ARCHIVE" }
      ]
      expiration_days = 365
      abort_incomplete_days = 7
    }
  ]
}

data "aws_caller_identity" "current" {}
```

**variables.tf**:
```hcl
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
```

**outputs.tf**:
```hcl
output "bucket_name" {
  description = "Name of the created bucket"
  value       = module.log_bucket.bucket_id
}

output "bucket_arn" {
  description = "ARN of the created bucket"
  value       = module.log_bucket.bucket_arn
}
```

## Testing the Setup

```bash
# Upload test log file
echo "Test log entry at $(date)" > test.log
aws s3 cp test.log s3://$(terraform output -raw bucket_name)/logs/test.log

# Verify upload
aws s3 ls s3://$(terraform output -raw bucket_name)/logs/

# Check lifecycle policy
aws s3api get-bucket-lifecycle-configuration \
    --bucket $(terraform output -raw bucket_name)
```

## Cost Estimation

For 100GB of logs per month:
- Month 1-2: ~$4.60 (STANDARD + STANDARD_IA)
- Month 3-6: ~$4.80 (includes GLACIER)
- Month 7-12: ~$2.97 (includes DEEP_ARCHIVE)
- **Total annual cost: ~$12.37**

Compare to keeping all in STANDARD: ~$276/year
**Savings: 95%**

## Cleanup

```bash
# Delete all objects first
aws s3 rm s3://$(terraform output -raw bucket_name) --recursive

# Destroy infrastructure
terraform destroy
```

## Next Steps

- See `examples/advanced/` for multi-region setup
- See `examples/compliance/` for enhanced compliance features
- Review `docs/manual/` for detailed explanations
