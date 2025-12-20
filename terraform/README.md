# Terraform Infrastructure

This directory contains the Terraform infrastructure as code for S3 log retention automation.

## Directory Structure

```
terraform/
├── main.tf              # Main configuration
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── providers.tf         # Provider configuration
├── backend.tf           # Backend configuration (create this)
├── environments/        # Environment-specific configurations
│   ├── dev.tfvars
│   ├── staging.tfvars
│   └── prod.tfvars
└── modules/            # Reusable modules
    ├── s3-bucket/
    ├── lifecycle-policy/
    ├── iam/
    ├── cloudwatch/
    └── sns/
```

## Getting Started

### 1. Initialize Terraform

```bash
terraform init
```

### 2. Validate Configuration

```bash
terraform validate
```

### 3. Plan Changes

```bash
terraform plan -var-file=environments/dev.tfvars
```

### 4. Apply Changes

```bash
terraform apply -var-file=environments/dev.tfvars
```

## Environment Management

Deploy to different environments:

```bash
# Development
terraform apply -var-file=environments/dev.tfvars

# Staging
terraform apply -var-file=environments/staging.tfvars

# Production
terraform apply -var-file=environments/prod.tfvars
```

## Module Usage

Each module can be used independently. See module-specific documentation for details.

### S3 Bucket Module

Creates a secure S3 bucket with encryption, versioning, and access logging.

### Lifecycle Policy Module

Manages S3 lifecycle rules for log retention and storage class transitions.

### IAM Module

Creates IAM roles and policies for S3 access.

### CloudWatch Module

Sets up monitoring dashboards and alarms.

### SNS Module

Configures SNS topics for alerting.

## Best Practices

1. Always use remote state (configure backend.tf)
2. Use separate workspaces or state files per environment
3. Review plan output before applying
4. Tag all resources appropriately
5. Enable versioning for state bucket
6. Use encrypted state storage

## Remote State Configuration

Create `backend.tf`:

```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "s3-log-retention/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

## Requirements

- Terraform >= 1.0
- AWS Provider ~> 5.0
- Valid AWS credentials configured

## Documentation

For detailed documentation, see:
- [Step-by-Step Guide](../docs/STEP_BY_STEP_GUIDE.md)
- [Architecture Documentation](../docs/architecture/)
- [Terraform Best Practices](../docs/terraform/best_practices.md)
