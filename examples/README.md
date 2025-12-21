# Examples

This directory contains example code demonstrating various use cases.

## Basic Examples

Simple examples for getting started:

- `basic/main.py` - Basic lifecycle policy creation
- `basic/upload_logs.py` - Uploading logs to S3

## Advanced Examples

More complex scenarios:

- `advanced/multi_environment.py` - Managing multiple environments
- `advanced/cost_optimization.py` - Cost analysis and optimization
- `advanced/compliance_reporting.py` - Generating compliance reports

## Multi-Account Examples

Enterprise scenarios:

- `multi-account/cross_account.py` - Cross-account log aggregation
- `multi-account/organization_wide.py` - AWS Organizations integration

## Running Examples

Each example is a standalone Python script:

```bash
cd examples/basic
python main.py
```

Update configuration variables in each script before running.

## Prerequisites

- AWS credentials configured
- S3 buckets created
- Python dependencies installed
- Configuration files updated

## Configuration

Examples use configuration from `configs/config.yaml`. Update this file with your settings.
This directory contains example configurations for deploying S3 log retention infrastructure.

## Available Examples

### Basic Example

**Directory**: `basic/`

Minimal deployment with core features:
- Single S3 bucket
- Standard lifecycle policy (365-day retention)
- AES256 encryption
- CloudWatch monitoring

**Use Case**: Small to medium deployments, testing, proof-of-concept

**Deploy**:
```bash
cd basic
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars
terraform init
terraform apply
```

### Advanced Example

**Directory**: `advanced/`

Full-featured deployment:
- KMS encryption
- Cross-account access
- Custom lifecycle rules
- Advanced monitoring with SNS
- Lambda integration

**Use Case**: Enterprise production environments

**Deploy**:
```bash
cd advanced
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars
terraform init
terraform apply
```

### Multi-Bucket Example

**Directory**: `multi_bucket/`

Multiple buckets with different policies:
- Separate buckets for different log types
- Different retention periods per bucket
- Centralized monitoring
- Shared IAM roles

**Use Case**: Organizations with multiple applications/services

**Deploy**:
```bash
cd multi_bucket
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars
terraform init
terraform apply
```

## Common Steps

1. **Navigate to example directory**:
   ```bash
   cd examples/<example-name>
   ```

2. **Copy example configuration**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. **Edit configuration**:
   ```bash
   # Update with your values
   vim terraform.tfvars
   ```

4. **Initialize Terraform**:
   ```bash
   terraform init
   ```

5. **Review plan**:
   ```bash
   terraform plan
   ```

6. **Apply configuration**:
   ```bash
   terraform apply
   ```

7. **Verify deployment**:
   ```bash
   terraform output
   aws s3 ls
   ```

## Cleanup

To destroy all resources:

```bash
cd examples/<example-name>
terraform destroy
```

Or use the cleanup script:
```bash
../../scripts/cleanup.sh <example-name>
```

## Customization

All examples can be customized by modifying `terraform.tfvars`:

- `bucket_name`: Change bucket name (must be globally unique)
- `retention_days`: Adjust retention period
- `aws_region`: Change AWS region
- `enable_monitoring`: Enable/disable CloudWatch monitoring
- `tags`: Add custom tags

## Quick Comparison

| Feature | Basic | Advanced | Multi-Bucket |
|---------|-------|----------|--------------|
| Encryption | AES256 | KMS | AES256/KMS |
| Monitoring | Basic | Advanced | Centralized |
| Cross-Account | No | Yes | Yes |
| Lambda | No | Yes | Optional |
| Complexity | Low | High | Medium |
| Cost | $ | $$$ | $$ |

## Getting Help

- See [QUICKSTART.md](../../QUICKSTART.md) for quick start guide
- See [MANUAL.md](../../MANUAL.md) for comprehensive documentation
- See [TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md) for common issues
