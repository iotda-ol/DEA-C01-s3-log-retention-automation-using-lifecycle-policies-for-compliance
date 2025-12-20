# Deployment Guide

Step-by-step guide for deploying S3 log retention automation.

## Pre-Deployment Checklist

- [ ] AWS account created and configured
- [ ] AWS CLI installed and configured
- [ ] Terraform installed (version 1.0+)
- [ ] Python 3.9+ installed
- [ ] Repository cloned locally
- [ ] Dependencies installed
- [ ] Environment variables configured

## Deployment Steps

### 1. Prepare Configuration

Edit the appropriate environment file:

```bash
# For development
vim terraform/environments/dev.tfvars

# For production
vim terraform/environments/prod.tfvars
```

Update these values:
```hcl
log_bucket_name = "your-unique-bucket-name-12345"
aws_region      = "us-east-1"
retention_days  = 365
alarm_email     = "your-email@example.com"
```

### 2. Initialize Terraform

```bash
cd terraform
terraform init
```

Expected output:
```
Initializing modules...
Initializing provider plugins...
Terraform has been successfully initialized!
```

### 3. Create State Backend (First Time Only)

Create an S3 bucket for Terraform state:

```bash
aws s3 mb s3://your-terraform-state-bucket --region us-east-1
aws s3api put-bucket-versioning \
  --bucket your-terraform-state-bucket \
  --versioning-configuration Status=Enabled
```

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

Create DynamoDB table for state locking:
```bash
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

Re-initialize:
```bash
terraform init -reconfigure
```

### 4. Validate Configuration

```bash
terraform validate
```

Expected output:
```
Success! The configuration is valid.
```

### 5. Plan Deployment

```bash
terraform plan -var-file=environments/dev.tfvars -out=tfplan
```

Review the plan carefully:
- Resources to be created
- No unexpected changes
- Correct configuration values

### 6. Apply Changes

```bash
terraform apply tfplan
```

Or with auto-approve (use carefully):
```bash
terraform apply -var-file=environments/dev.tfvars -auto-approve
```

### 7. Verify Deployment

```bash
# Check bucket creation
aws s3 ls | grep log-retention

# Check lifecycle policy
aws s3api get-bucket-lifecycle-configuration \
  --bucket your-bucket-name

# Run validation script
python scripts/validate_infrastructure.py your-bucket-name
```

### 8. Test Functionality

```bash
# Upload test logs
python scripts/test_lifecycle.py your-bucket-name 10

# Use CLI
s3-log-retention list-logs --bucket your-bucket-name
s3-log-retention validate-policy --bucket your-bucket-name
```

## Post-Deployment

### Configure Monitoring

1. Check CloudWatch dashboard is created
2. Verify alarms are active
3. Confirm SNS subscriptions (check email)

### Document Deployment

Record:
- Deployment date and time
- Terraform version used
- Environment deployed
- Bucket names created
- Any issues encountered

### Set Up Backups

Enable cross-region replication (optional):
```bash
terraform apply -var-file=environments/prod.tfvars \
  -var enable_replication=true \
  -var replication_region=us-west-2
```

## Multi-Environment Deployment

### Development

```bash
terraform workspace new dev
terraform apply -var-file=environments/dev.tfvars
```

### Staging

```bash
terraform workspace new staging
terraform apply -var-file=environments/staging.tfvars
```

### Production

```bash
terraform workspace new prod
terraform apply -var-file=environments/prod.tfvars
```

## Rollback Procedure

If deployment fails:

```bash
# Show current state
terraform show

# Destroy problematic resources
terraform destroy -target=module.s3_bucket

# Fix configuration
vim terraform/main.tf

# Re-apply
terraform apply -var-file=environments/dev.tfvars
```

## Troubleshooting

### Bucket name already exists

```
Error: Error creating S3 bucket: BucketAlreadyExists
```

Solution: Choose a different bucket name (must be globally unique)

### Insufficient permissions

```
Error: error creating S3 bucket: AccessDenied
```

Solution: Check IAM permissions, ensure you have s3:CreateBucket

### State lock timeout

```
Error: Error acquiring the state lock
```

Solution:
```bash
# Force unlock (use carefully)
terraform force-unlock <lock-id>

# Or delete lock manually
aws dynamodb delete-item \
  --table-name terraform-state-lock \
  --key '{"LockID": {"S": "<lock-id>"}}'
```

## Maintenance

### Update Infrastructure

```bash
# Pull latest changes
git pull origin main

# Review changes
terraform plan -var-file=environments/prod.tfvars

# Apply updates
terraform apply -var-file=environments/prod.tfvars
```

### Destroy Resources

To completely remove infrastructure:

```bash
# Review what will be destroyed
terraform plan -destroy -var-file=environments/dev.tfvars

# Destroy
terraform destroy -var-file=environments/dev.tfvars
```

**Warning**: This will delete all logs in the bucket!

## Best Practices

1. **Always review plan** before applying
2. **Use workspaces** for multiple environments
3. **Enable state locking** to prevent conflicts
4. **Backup state files** regularly
5. **Tag resources** appropriately
6. **Document changes** in git commits
7. **Test in dev** before prod deployment
8. **Monitor costs** after deployment

## CI/CD Integration

For automated deployments, see `.github/workflows/main.yml`

## Next Steps

1. Configure alerting (CloudWatch alarms)
2. Set up log ingestion pipeline
3. Create operational runbooks
4. Schedule compliance audits
5. Train team on operations
