# Troubleshooting Guide

## Common Issues and Solutions

### AWS Configuration Issues

#### Error: "Unable to locate credentials"

**Problem**: AWS CLI is not configured with credentials.

**Solution**:
```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

#### Error: "Access Denied" when creating bucket

**Problem**: IAM user lacks necessary permissions.

**Solution**: Ensure your IAM user has the following permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:PutBucketLifecycleConfiguration",
        "s3:PutBucketEncryption",
        "s3:PutBucketVersioning",
        "s3:PutBucketPublicAccessBlock"
      ],
      "Resource": "arn:aws:s3:::*"
    }
  ]
}
```

---

### Terraform Issues

#### Error: "Bucket name already exists"

**Problem**: S3 bucket names must be globally unique.

**Solution**:
```bash
# Edit terraform.tfvars and change bucket_name
bucket_name = "my-unique-bucket-name-12345"
```

#### Error: "No such lifecycle configuration"

**Problem**: Trying to get lifecycle config before it's created.

**Solution**: This is normal during initial deployment. Wait for `terraform apply` to complete.

#### Error: "State lock acquisition failed"

**Problem**: Another Terraform process is running or crashed.

**Solution**:
```bash
# Force unlock (use with caution)
terraform force-unlock <LOCK_ID>

# Or configure DynamoDB for state locking
```

---

### Python Issues

#### Error: "ModuleNotFoundError: No module named 'boto3'"

**Problem**: Python dependencies not installed.

**Solution**:
```bash
# Install dependencies
pip install -r python/requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r python/requirements.txt
```

#### Error: "ClientError: An error occurred (NoSuchBucket)"

**Problem**: Bucket doesn't exist or name is incorrect.

**Solution**:
```bash
# List existing buckets
aws s3 ls

# Check bucket name in your code/config
python3 -m python.src.cli.main list-buckets
```

---

### Lifecycle Policy Issues

#### Logs not transitioning to Glacier

**Problem**: Objects haven't reached the configured age yet.

**Solution**: Lifecycle transitions happen asynchronously. Check:
```bash
# Verify policy is configured
aws s3api get-bucket-lifecycle-configuration --bucket <bucket-name>

# Check object age
aws s3api list-objects-v2 --bucket <bucket-name> --query 'Contents[*].[Key,LastModified]'
```

#### Objects not being deleted after retention period

**Problem**: Policy may not be properly configured or objects haven't reached expiration.

**Solution**:
```bash
# Verify expiration rule
aws s3api get-bucket-lifecycle-configuration --bucket <bucket-name>

# Use Python validator
python3 -m python.src.cli.main validate-policy <bucket-name>
```

---

### Validation Issues

#### Validation shows "Non-compliant"

**Problem**: Lifecycle policy doesn't meet compliance requirements.

**Solution**:
```bash
# Check current retention period
python3 -m python.src.cli.main validate-policy <bucket-name>

# Update retention period in terraform.tfvars
retention_days = 365  # Minimum for compliance

# Apply changes
terraform apply
```

---

### Script Issues

#### Error: "Permission denied" when running scripts

**Problem**: Scripts don't have execute permissions.

**Solution**:
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Or run with bash
bash scripts/deploy.sh
```

#### Deploy script fails at plan stage

**Problem**: Configuration errors in Terraform files.

**Solution**:
```bash
# Validate configuration
cd examples/basic
terraform validate

# Check for syntax errors
terraform fmt -check
```

---

### Monitoring Issues

#### CloudWatch dashboard not showing data

**Problem**: Metrics may take time to populate, or monitoring not enabled.

**Solution**:
```bash
# Verify monitoring is enabled
cd examples/basic
grep enable_monitoring terraform.tfvars

# Wait 5-10 minutes for metrics to populate
# Or upload some test files to generate metrics
aws s3 cp test.log s3://<bucket-name>/test.log
```

#### Alarms not triggering

**Problem**: Alarm actions not configured or thresholds not reached.

**Solution**:
```bash
# Check alarm configuration
aws cloudwatch describe-alarms --alarm-names "<bucket-name>-size-alarm"

# Verify SNS topic is configured
aws sns list-subscriptions
```

---

### Cost Issues

#### Unexpected costs

**Problem**: Objects not transitioning to cheaper storage classes.

**Solution**:
```bash
# Check storage class distribution
aws s3api list-objects-v2 --bucket <bucket-name> \
  --query 'Contents[*].[Key,StorageClass]' --output table

# Review lifecycle policy
python3 -m python.src.cli.main validate-policy <bucket-name>

# Generate cost report
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

---

### Testing Issues

#### Unit tests failing

**Problem**: Dependencies not installed or mocks not configured.

**Solution**:
```bash
# Install test dependencies
pip install -r python/requirements.txt

# Run specific test
pytest python/tests/unit/test_s3_client.py::test_list_buckets -v

# Check test output for specific error
pytest python/tests/unit/ -v --tb=long
```

---

## Best Practices

### Before Deployment

1. **Test in Non-Production**: Always test in dev/staging first
2. **Review Plan**: Check `terraform plan` output carefully
3. **Backup Configuration**: Keep terraform.tfvars in version control (without secrets)
4. **Validate Compliance**: Run validation before going live

### During Operations

1. **Regular Monitoring**: Check CloudWatch dashboards weekly
2. **Compliance Audits**: Run compliance reports monthly
3. **Cost Review**: Review storage costs monthly
4. **Update Dependencies**: Keep Terraform and Python packages updated

### Troubleshooting Workflow

1. **Check Logs**: Review CloudWatch logs and Terraform output
2. **Verify Configuration**: Validate terraform files and Python code
3. **Test Incrementally**: Make small changes and test
4. **Use Debugging**: Enable verbose logging with `--verbose` flag
5. **Consult Documentation**: Review MANUAL.md and AWS documentation

---

## Getting Help

### Resources

- **Project Documentation**: See `/docs` folder
- **AWS Documentation**: https://docs.aws.amazon.com/s3/
- **Terraform Docs**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **GitHub Issues**: Report bugs and ask questions

### Debug Commands

```bash
# Terraform debugging
export TF_LOG=DEBUG
terraform plan

# Python debugging
python3 -m python.src.cli.main --verbose list-buckets

# AWS CLI debugging
aws s3 ls --debug

# Check CloudWatch logs
aws logs tail /aws/lambda/<function-name> --follow
```

### Contact

- GitHub Issues: For bugs and feature requests
- Discussions: For questions and general help
- Security: Report security issues privately

---

## Quick Reference

### Validation Checklist

- [ ] AWS credentials configured
- [ ] Terraform installed and initialized
- [ ] Python dependencies installed
- [ ] Bucket name is unique
- [ ] Region is set correctly
- [ ] Lifecycle policy meets compliance (365 days)
- [ ] Encryption is enabled
- [ ] Public access is blocked
- [ ] Monitoring is configured

### Recovery Commands

```bash
# Rollback Terraform changes
terraform state pull > backup.tfstate
terraform state push backup.tfstate

# Restore deleted objects (if versioning enabled)
aws s3api list-object-versions --bucket <bucket-name>
aws s3api copy-object --copy-source <bucket>/<key>?versionId=<id>

# Emergency cleanup
./scripts/cleanup.sh basic
```
