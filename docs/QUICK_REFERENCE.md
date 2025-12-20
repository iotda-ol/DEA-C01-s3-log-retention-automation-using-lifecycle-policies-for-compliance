# Quick Reference Guide

## Common Commands

### Python CLI

```bash
# List all buckets
python python/main.py list-buckets

# Check lifecycle policy
python python/main.py check-policy BUCKET_NAME

# Apply standard compliance policy
python python/main.py apply-policy BUCKET_NAME

# Apply custom policy
python python/main.py apply-policy BUCKET_NAME \
  --retention-days 730 \
  --glacier-days 180 \
  --ia-days 60

# Validate compliance
python python/main.py validate BUCKET_NAME

# Scan all buckets
python python/main.py scan-all

# Export policy to file
python python/main.py export-policy BUCKET_NAME policy.json

# Import policy from file
python python/main.py import-policy BUCKET_NAME policy.json
```

### Terraform

```bash
# Initialize
cd terraform/environments/dev
terraform init

# Validate
terraform validate

# Plan
terraform plan

# Apply
terraform apply

# Destroy
terraform destroy
```

### Python Examples

```bash
# Run basic examples
python examples/basic/list_buckets.py
python examples/basic/apply_lifecycle.py
python examples/basic/validate_compliance.py
```

## Configuration Files

### Python Config (config/dev/config.yaml)

```yaml
aws:
  region: us-east-1
  profile: default

s3:
  retention_days: 365
  enable_transitions: true

compliance:
  required_retention_days: 365
  require_encryption: true
```

### Terraform Config (terraform/environments/dev/terraform.tfvars)

```hcl
environment      = "dev"
retention_days   = 365
enable_versioning = true
enable_encryption = true
```

## Module Usage

### S3 Bucket Module

```hcl
module "log_bucket" {
  source = "../../modules/s3-bucket"

  bucket_name        = "my-log-bucket"
  environment        = "prod"
  enable_versioning  = true
  enable_encryption  = true
}
```

### Lifecycle Policy Module

```hcl
module "lifecycle" {
  source = "../../modules/lifecycle-policy"

  bucket_id                 = module.log_bucket.bucket_id
  retention_days            = 365
  enable_glacier_transition = true
  glacier_transition_days   = 90
}
```

### IAM Module

```hcl
module "s3_role" {
  source = "../../modules/iam"

  role_name   = "s3-access"
  services    = ["ec2.amazonaws.com"]
  bucket_arns = [module.log_bucket.bucket_arn]
}
```

## Python API

### S3 Operations

```python
from s3_operations.client import S3Operations

s3 = S3Operations(region='us-east-1')

# List buckets
buckets = s3.list_buckets()

# Check if bucket exists
exists = s3.bucket_exists('my-bucket')

# Upload file
s3.upload_file('local.log', 'my-bucket', 'logs/file.log')

# Download file
s3.download_file('my-bucket', 'logs/file.log', 'local.log')
```

### Lifecycle Management

```python
from lifecycle_management.manager import LifecycleManager

mgr = LifecycleManager(region='us-east-1')

# Get policy
policy = mgr.get_lifecycle_policy('my-bucket')

# Create compliance rule
rule = mgr.create_compliance_rule(
    retention_days=365,
    enable_glacier=True,
    glacier_days=90
)

# Apply policy
mgr.set_lifecycle_policy('my-bucket', [rule])
```

### Compliance Validation

```python
from compliance.validator import ComplianceValidator
import boto3

validator = ComplianceValidator(required_retention_days=365)
s3_client = boto3.client('s3')

# Validate bucket
results = validator.validate_bucket('my-bucket', s3_client)

if results['compliant']:
    print("Bucket is compliant")
else:
    print("Issues found:")
    for check, result in results['checks'].items():
        if not result['compliant']:
            print(f"  {check}: {result['issues']}")
```

## Troubleshooting

### AWS Credentials Not Configured

```bash
aws configure
# Enter Access Key ID, Secret, Region
```

### Python Dependencies Missing

```bash
cd python
pip install -r requirements.txt
```

### Permission Denied on Scripts

```bash
chmod +x scripts/setup.sh
chmod +x python/main.py
```

### Terraform Module Not Found

```bash
cd terraform/environments/dev
terraform init
```

## Environment Variables

```bash
# Set AWS profile
export AWS_PROFILE=dev

# Set AWS region
export AWS_DEFAULT_REGION=us-east-1

# Python path
export PYTHONPATH=/path/to/project/python/src
```

## File Locations

- **Documentation**: `docs/INSTRUCTIONS.md`
- **Python CLI**: `python/main.py`
- **Terraform Modules**: `terraform/modules/`
- **Config Files**: `config/dev/`
- **Examples**: `examples/basic/`
- **Tests**: `python/tests/`
