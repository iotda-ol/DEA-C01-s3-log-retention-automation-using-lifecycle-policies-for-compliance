# Troubleshooting Guide

Common issues and solutions for S3 Log Retention Automation.

## Table of Contents
- [Terraform Issues](#terraform-issues)
- [Python/Boto3 Issues](#pythonboto3-issues)
- [AWS Permissions Issues](#aws-permissions-issues)
- [Lifecycle Policy Issues](#lifecycle-policy-issues)
- [Cost Issues](#cost-issues)
- [Monitoring Issues](#monitoring-issues)

---

## Terraform Issues

### Error: Backend initialization failed

**Symptom**:
```
Error: Failed to get existing workspaces: S3 bucket does not exist
```

**Solution**:
```bash
# Create the state bucket first
aws s3 mb s3://terraform-state-bucket

# Enable versioning on state bucket
aws s3api put-bucket-versioning \
    --bucket terraform-state-bucket \
    --versioning-configuration Status=Enabled

# Create DynamoDB table for locking
aws dynamodb create-table \
    --table-name terraform-locks \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

### Error: Resource already exists

**Symptom**:
```
Error: error creating S3 bucket: BucketAlreadyExists
```

**Solution**:
```bash
# Import existing resource
terraform import module.log_bucket.aws_s3_bucket.log_bucket BUCKET_NAME

# Or use a unique bucket name
# Add account ID to bucket name in variables
```

### Error: Provider configuration not found

**Symptom**:
```
Error: Provider configuration not present
```

**Solution**:
```bash
# Initialize with upgrade flag
terraform init -upgrade

# Verify provider is specified in required_providers
```

---

## Python/Boto3 Issues

### Error: Unable to locate credentials

**Symptom**:
```python
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**Solutions**:
```bash
# Option 1: Configure AWS CLI
aws configure

# Option 2: Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Option 3: Use AWS profile
export AWS_PROFILE=your-profile-name

# Verify credentials
aws sts get-caller-identity
```

### Error: Import errors

**Symptom**:
```python
ModuleNotFoundError: No module named 'boto3'
```

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r python/requirements.txt

# Verify installation
python -c "import boto3; print(boto3.__version__)"
```

### Error: Region not specified

**Symptom**:
```python
botocore.exceptions.NoRegionError: You must specify a region
```

**Solution**:
```python
# Specify region in code
import boto3
s3 = boto3.client('s3', region_name='us-east-1')

# Or set environment variable
export AWS_DEFAULT_REGION=us-east-1

# Or configure in ~/.aws/config
[default]
region = us-east-1
```

---

## AWS Permissions Issues

### Error: Access Denied

**Symptom**:
```
An error occurred (AccessDenied) when calling the PutObject operation
```

**Solution**:

1. **Check IAM permissions**:
```bash
# List user's policies
aws iam list-attached-user-policies --user-name YOUR_USER

# Check policy document
aws iam get-policy-version \
    --policy-arn arn:aws:iam::123456:policy/S3LogRetentionPolicy \
    --version-id v1
```

2. **Required minimum permissions**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutBucketVersioning",
        "s3:PutLifecycleConfiguration",
        "s3:GetLifecycleConfiguration"
      ],
      "Resource": [
        "arn:aws:s3:::*log*",
        "arn:aws:s3:::*log*/*"
      ]
    }
  ]
}
```

### Error: Bucket policy conflicts

**Symptom**:
```
Error: Error putting S3 policy: MalformedPolicy
```

**Solution**:
```bash
# Validate policy JSON
cat bucket-policy.json | jq .

# Test policy with IAM Policy Simulator
# AWS Console → IAM → Policy Simulator

# Remove conflicting statements
aws s3api delete-bucket-policy --bucket BUCKET_NAME
```

---

## Lifecycle Policy Issues

### Error: Lifecycle rule validation failed

**Symptom**:
```
InvalidArgument: Lifecycle rule transition days must be greater than 0
```

**Solution**:
- Ensure transition days are positive integers
- STANDARD_IA requires minimum 30 days
- Transitions must be in ascending order
- Cannot skip storage classes

**Correct order**:
```json
{
  "Transitions": [
    {"Days": 30, "StorageClass": "STANDARD_IA"},
    {"Days": 90, "StorageClass": "GLACIER"},
    {"Days": 180, "StorageClass": "DEEP_ARCHIVE"}
  ]
}
```

### Objects not transitioning

**Symptom**: Objects remain in STANDARD after 30 days

**Solutions**:
1. **Check lifecycle policy exists**:
```bash
aws s3api get-bucket-lifecycle-configuration --bucket BUCKET_NAME
```

2. **Verify object matches filter**:
```bash
# List objects with storage class
aws s3api list-objects-v2 \
    --bucket BUCKET_NAME \
    --query 'Contents[*].[Key,StorageClass,LastModified]' \
    --output table
```

3. **Check object age**: Lifecycle evaluates once daily (UTC midnight)

4. **Verify minimum size**: Objects < 128KB may not transition to IA

### Cannot delete lifecycle policy

**Symptom**:
```
NoSuchLifecycleConfiguration: The lifecycle configuration does not exist
```

**Solution**:
```bash
# Lifecycle policy already removed, or never existed
# Verify bucket name is correct
aws s3 ls | grep BUCKET_NAME
```

---

## Cost Issues

### Unexpected high costs

**Symptom**: S3 costs higher than expected

**Investigation**:
```bash
# Check total bucket size
aws cloudwatch get-metric-statistics \
    --namespace AWS/S3 \
    --metric-name BucketSizeBytes \
    --dimensions Name=BucketName,Value=BUCKET_NAME Name=StorageType,Value=StandardStorage \
    --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 86400 \
    --statistics Average

# Check number of objects
aws cloudwatch get-metric-statistics \
    --namespace AWS/S3 \
    --metric-name NumberOfObjects \
    --dimensions Name=BucketName,Value=BUCKET_NAME Name=StorageType,Value=AllStorageTypes \
    --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 86400 \
    --statistics Average

# Use Cost Explorer
# AWS Console → Billing → Cost Explorer
# Filter by Service = S3
```

**Common causes**:
- Objects not transitioning (see above)
- Retrieval fees from Glacier
- Many small objects (minimum billable size)
- Incomplete multipart uploads
- Many API requests

**Solutions**:
```bash
# Clean up incomplete multipart uploads
aws s3api list-multipart-uploads --bucket BUCKET_NAME

# Add lifecycle rule to abort
{
  "AbortIncompleteMultipartUpload": {
    "DaysAfterInitiation": 7
  }
}

# Use S3 Inventory for detailed analysis
```

---

## Monitoring Issues

### CloudWatch alarms not triggering

**Symptom**: Storage quota exceeded but no alarm

**Solutions**:
1. **Verify alarm exists**:
```bash
aws cloudwatch describe-alarms \
    --alarm-names BUCKET_NAME-storage-quota
```

2. **Check alarm state**:
```bash
aws cloudwatch describe-alarm-history \
    --alarm-name BUCKET_NAME-storage-quota \
    --history-item-type StateUpdate \
    --max-records 5
```

3. **Verify SNS subscription**:
```bash
aws sns list-subscriptions-by-topic \
    --topic-arn arn:aws:sns:us-east-1:123456:alerts

# Confirm subscription in email
```

### No CloudWatch metrics

**Symptom**: BucketSizeBytes metric missing

**Solution**:
- CloudWatch metrics for S3 updated daily
- Wait 24 hours after bucket creation
- Metrics only available for buckets with objects
- Check correct region

### CloudTrail not logging

**Symptom**: No S3 API calls in CloudTrail

**Solutions**:
```bash
# Verify trail is logging
aws cloudtrail get-trail-status --name TRAIL_NAME

# Start logging if stopped
aws cloudtrail start-logging --name TRAIL_NAME

# Check data events are configured
aws cloudtrail get-event-selectors --trail-name TRAIL_NAME

# Verify S3 bucket policy allows CloudTrail
```

---

## Getting Help

If issues persist:

1. **Check AWS Service Health Dashboard**: https://status.aws.amazon.com/
2. **Review AWS Documentation**: https://docs.aws.amazon.com/s3/
3. **Search GitHub Issues**: Existing solutions may be available
4. **Open New Issue**: Include error messages, configurations, and steps to reproduce
5. **AWS Support**: For AWS-specific issues (requires support plan)

## Debugging Tips

### Enable Debug Logging

**Boto3**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Terraform**:
```bash
export TF_LOG=DEBUG
terraform apply
```

**AWS CLI**:
```bash
aws s3 ls --debug
```

### Verify Configurations

```bash
# Check Terraform state
terraform state list
terraform state show MODULE.RESOURCE

# Validate JSON
cat config.json | jq .

# Test IAM policy
aws iam simulate-principal-policy \
    --policy-source-arn USER_ARN \
    --action-names s3:PutObject \
    --resource-arns arn:aws:s3:::bucket/key
```
