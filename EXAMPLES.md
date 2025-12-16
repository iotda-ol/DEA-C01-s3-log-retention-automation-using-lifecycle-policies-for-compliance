# Usage Examples

This document provides practical examples for using the S3 log retention automation solution.

## Table of Contents

- [Basic Deployment](#basic-deployment)
- [Advanced Configuration](#advanced-configuration)
- [Writing Logs](#writing-logs)
- [Monitoring](#monitoring)
- [Testing Lifecycle Policies](#testing-lifecycle-policies)

## Basic Deployment

### Minimal Configuration

Deploy with default settings (1-year retention, cost optimization enabled):

1. Create `terraform.tfvars`:
   ```hcl
   bucket_name = "my-company-logs-2024"
   aws_region  = "us-east-1"
   ```

2. Deploy:
   ```bash
   terraform init
   terraform apply
   ```

### Custom Retention Period

For 2-year retention (730 days):

```hcl
bucket_name    = "my-company-logs-2024"
retention_days = 730
transition_to_ia_days = 180      # Transition to IA after 6 months
transition_to_glacier_days = 365  # Transition to Glacier after 1 year
```

### Disable Storage Class Transitions

Keep logs in STANDARD storage class throughout retention:

```hcl
bucket_name               = "my-company-logs-2024"
retention_days            = 365
transition_to_ia_days     = 366  # Set higher than retention_days
transition_to_glacier_days = 366  # Set higher than retention_days
```

## Advanced Configuration

### Using KMS Encryption

Create a KMS key and use it for encryption:

```bash
# Create KMS key
KMS_KEY_ID=$(aws kms create-key \
  --description "S3 log encryption key" \
  --query 'KeyMetadata.KeyId' \
  --output text)

# Add to terraform.tfvars
echo "kms_key_id = \"${KMS_KEY_ID}\"" >> terraform.tfvars

# Deploy
terraform apply
```

### Multi-Environment Setup

Use workspaces for different environments:

```bash
# Production
terraform workspace new production
cat > terraform.tfvars <<EOF
bucket_name = "prod-logs-bucket"
tags = {
  Environment = "production"
  Compliance  = "1-year-retention"
}
EOF
terraform apply

# Staging
terraform workspace new staging
cat > terraform.tfvars <<EOF
bucket_name = "staging-logs-bucket"
retention_days = 90  # Shorter retention for staging
tags = {
  Environment = "staging"
  Compliance  = "90-day-retention"
}
EOF
terraform apply
```

### Custom Tagging Strategy

```hcl
bucket_name = "my-company-logs-2024"

tags = {
  Environment  = "production"
  Purpose      = "log-retention"
  Compliance   = "1-year-retention"
  ManagedBy    = "terraform"
  CostCenter   = "engineering"
  DataClass    = "confidential"
  Owner        = "platform-team@example.com"
  Project      = "log-management"
  Department   = "IT"
  Backup       = "not-required"
}
```

## Writing Logs

### From EC2 Instances

#### Using AWS CLI

```bash
#!/bin/bash
# log-to-s3.sh - Script to upload logs to S3

BUCKET_NAME=$(terraform output -raw bucket_id)
LOG_FILE="/var/log/application.log"
DATE_PATH=$(date +%Y/%m/%d)
TIMESTAMP=$(date +%H%M%S)

aws s3 cp "$LOG_FILE" \
  "s3://${BUCKET_NAME}/logs/${DATE_PATH}/application-${TIMESTAMP}.log" \
  --metadata "source=ec2,instance=$(ec2-metadata --instance-id | cut -d' ' -f2)"
```

#### Using Fluent Bit

Create `/etc/fluent-bit/fluent-bit.conf`:

```ini
[SERVICE]
    Flush        5
    Daemon       Off
    Log_Level    info

[INPUT]
    Name         tail
    Path         /var/log/application.log
    Tag          app.logs

[OUTPUT]
    Name                s3
    Match               *
    bucket              my-company-logs-2024
    region              us-east-1
    total_file_size     10M
    upload_timeout      1m
    s3_key_format       /logs/%Y/%m/%d/$UUID.log
    compression         gzip
```

Start Fluent Bit:
```bash
fluent-bit -c /etc/fluent-bit/fluent-bit.conf
```

### From Lambda Functions

#### Python Example

```python
import boto3
import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
BUCKET_NAME = 'my-company-logs-2024'

def lambda_handler(event, context):
    # Your application logic here
    try:
        # Generate log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'function_name': context.function_name,
            'request_id': context.request_id,
            'event': event,
            'status': 'success'
        }
        
        # Write log to S3
        date_path = datetime.now().strftime('%Y/%m/%d')
        log_key = f"logs/{date_path}/{context.request_id}.json"
        
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=log_key,
            Body=json.dumps(log_entry),
            ContentType='application/json'
        )
        
        logger.info(f"Log written to s3://{BUCKET_NAME}/{log_key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise
```

#### Node.js Example

```javascript
const AWS = require('aws-sdk');
const s3 = new AWS.S3();

const BUCKET_NAME = 'my-company-logs-2024';

exports.handler = async (event, context) => {
    try {
        const logEntry = {
            timestamp: new Date().toISOString(),
            functionName: context.functionName,
            requestId: context.requestId,
            event: event,
            status: 'success'
        };
        
        const now = new Date();
        const datePath = `${now.getFullYear()}/${String(now.getMonth() + 1).padStart(2, '0')}/${String(now.getDate()).padStart(2, '0')}`;
        const logKey = `logs/${datePath}/${context.requestId}.json`;
        
        await s3.putObject({
            Bucket: BUCKET_NAME,
            Key: logKey,
            Body: JSON.stringify(logEntry),
            ContentType: 'application/json'
        }).promise();
        
        console.log(`Log written to s3://${BUCKET_NAME}/${logKey}`);
        
        return {
            statusCode: 200,
            body: JSON.stringify('Success')
        };
        
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
```

### From ECS/Fargate

#### Using FireLens (Fluent Bit)

Task definition snippet:

```json
{
  "family": "my-app",
  "taskRoleArn": "arn:aws:iam::123456789012:role/log-writer-role",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "my-app:latest",
      "logConfiguration": {
        "logDriver": "awsfirelens",
        "options": {
          "Name": "s3",
          "region": "us-east-1",
          "bucket": "my-company-logs-2024",
          "total_file_size": "10M",
          "s3_key_format": "/logs/%Y/%m/%d/$UUID.log",
          "compression": "gzip"
        }
      }
    },
    {
      "name": "log_router",
      "image": "amazon/aws-for-fluent-bit:latest",
      "firelensConfiguration": {
        "type": "fluentbit"
      }
    }
  ]
}
```

### From CloudWatch Logs

Export CloudWatch Logs to S3:

```bash
#!/bin/bash
# export-cloudwatch-logs.sh

LOG_GROUP_NAME="/aws/lambda/my-function"
BUCKET_NAME=$(terraform output -raw bucket_id)
START_TIME=$(date -d '1 day ago' +%s)000
END_TIME=$(date +%s)000

aws logs create-export-task \
  --log-group-name "$LOG_GROUP_NAME" \
  --from "$START_TIME" \
  --to "$END_TIME" \
  --destination "$BUCKET_NAME" \
  --destination-prefix "cloudwatch-exports/"
```

## Monitoring

### CloudWatch Alarms

Create alarms for bucket monitoring:

```bash
# Alert on high number of PUT requests
aws cloudwatch put-metric-alarm \
  --alarm-name s3-high-put-requests \
  --alarm-description "Alert on high PUT request rate" \
  --metric-name NumberOfObjects \
  --namespace AWS/S3 \
  --statistic Average \
  --period 300 \
  --threshold 10000 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=BucketName,Value=$(terraform output -raw bucket_id) \
                Name=StorageType,Value=AllStorageTypes

# Alert on bucket size
aws cloudwatch put-metric-alarm \
  --alarm-name s3-bucket-size \
  --alarm-description "Alert on bucket size exceeding threshold" \
  --metric-name BucketSizeBytes \
  --namespace AWS/S3 \
  --statistic Average \
  --period 86400 \
  --threshold 1099511627776 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=BucketName,Value=$(terraform output -raw bucket_id) \
                Name=StorageType,Value=StandardStorage
```

### Viewing Metrics

```bash
# Get bucket size
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name BucketSizeBytes \
  --dimensions Name=BucketName,Value=$(terraform output -raw bucket_id) \
               Name=StorageType,Value=StandardStorage \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average

# Get number of objects
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name NumberOfObjects \
  --dimensions Name=BucketName,Value=$(terraform output -raw bucket_id) \
               Name=StorageType,Value=AllStorageTypes \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average
```

### S3 Inventory Reports

Enable S3 Inventory for detailed object reports:

```bash
aws s3api put-bucket-inventory-configuration \
  --bucket $(terraform output -raw bucket_id) \
  --id daily-inventory \
  --inventory-configuration '{
    "Destination": {
      "S3BucketDestination": {
        "AccountId": "'$(aws sts get-caller-identity --query Account --output text)'",
        "Bucket": "arn:aws:s3:::'$(terraform output -raw bucket_id)'",
        "Format": "CSV",
        "Prefix": "inventory/"
      }
    },
    "IsEnabled": true,
    "Id": "daily-inventory",
    "IncludedObjectVersions": "Current",
    "Schedule": {
      "Frequency": "Daily"
    }
  }'
```

## Testing Lifecycle Policies

### Test with Shorter Retention

Create a test bucket with short retention for validation:

```hcl
# test.tfvars
bucket_name               = "test-logs-bucket-short-retention"
retention_days            = 2  # 2 days for testing
transition_to_ia_days     = 1  # 1 day for testing
transition_to_glacier_days = 3  # Set higher to skip Glacier in test
```

Deploy and test:

```bash
terraform apply -var-file=test.tfvars

# Upload test object
echo "test log entry" > test.log
aws s3 cp test.log s3://test-logs-bucket-short-retention/test.log

# Check object after 1 day - should be in STANDARD_IA
aws s3api head-object \
  --bucket test-logs-bucket-short-retention \
  --key test.log \
  --query 'StorageClass'

# Check after 2 days - object should be deleted
aws s3api head-object \
  --bucket test-logs-bucket-short-retention \
  --key test.log
# Should return 404 Not Found
```

### Verify Lifecycle Configuration

```bash
# Get lifecycle configuration
aws s3api get-bucket-lifecycle-configuration \
  --bucket $(terraform output -raw bucket_id) | jq '.'

# Verify specific rule
aws s3api get-bucket-lifecycle-configuration \
  --bucket $(terraform output -raw bucket_id) | \
  jq '.Rules[] | select(.ID=="log-retention-policy")'
```

### Manual Transition Testing

Manually transition an object to test storage classes:

```bash
# Upload test object
echo "test" > test.log
aws s3 cp test.log s3://$(terraform output -raw bucket_id)/test.log

# Manually transition to STANDARD_IA
aws s3api copy-object \
  --bucket $(terraform output -raw bucket_id) \
  --copy-source $(terraform output -raw bucket_id)/test.log \
  --key test.log \
  --storage-class STANDARD_IA \
  --metadata-directive COPY

# Verify storage class
aws s3api head-object \
  --bucket $(terraform output -raw bucket_id) \
  --key test.log \
  --query 'StorageClass'
```

## Real-World Scenarios

### Scenario 1: Application Server Logs

```bash
# Nginx access logs
aws s3 sync /var/log/nginx/ \
  s3://$(terraform output -raw bucket_id)/nginx-logs/$(hostname)/$(date +%Y/%m/%d)/ \
  --exclude "*" --include "access.log*" --exclude "*.gz"

# Rotate and compress
logrotate /etc/logrotate.d/nginx
```

### Scenario 2: Database Audit Logs

```bash
# PostgreSQL logs
pg_dump_log() {
  PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d postgres \
    -c "SELECT * FROM pg_stat_activity" > /tmp/pg_activity.log
  
  aws s3 cp /tmp/pg_activity.log \
    s3://$(terraform output -raw bucket_id)/database-logs/postgresql/$(date +%Y/%m/%d/%H%M%S).log
}
```

### Scenario 3: Security Event Logs

```bash
# VPC Flow Logs to S3 (already configured in AWS)
# Just ensure they go to our managed bucket

# GuardDuty findings export
aws guardduty create-publishing-destination \
  --detector-id $DETECTOR_ID \
  --destination-type S3 \
  --destination-properties DestinationArn=arn:aws:s3:::$(terraform output -raw bucket_id)/guardduty/,KmsKeyArn=$KMS_KEY_ARN
```

## Troubleshooting

### Issue: Objects Not Being Deleted

```bash
# Check object age
aws s3api list-objects-v2 \
  --bucket $(terraform output -raw bucket_id) \
  --query 'Contents[?LastModified<=`2023-01-01T00:00:00.000Z`].[Key,LastModified]' \
  --output table

# Check lifecycle rules are enabled
aws s3api get-bucket-lifecycle-configuration \
  --bucket $(terraform output -raw bucket_id) | \
  jq '.Rules[] | {ID: .ID, Status: .Status}'
```

### Issue: Access Denied

```bash
# Verify IAM permissions
aws iam simulate-principal-policy \
  --policy-source-arn $(terraform output -raw log_writer_role_arn) \
  --action-names s3:PutObject s3:ListBucket \
  --resource-arns \
    "arn:aws:s3:::$(terraform output -raw bucket_id)/*" \
    "arn:aws:s3:::$(terraform output -raw bucket_id)"
```

### Issue: High Costs

```bash
# Analyze storage class distribution
aws s3api list-objects-v2 \
  --bucket $(terraform output -raw bucket_id) \
  --query 'Contents[*].[StorageClass]' | \
  sort | uniq -c

# Check for incomplete multipart uploads
aws s3api list-multipart-uploads \
  --bucket $(terraform output -raw bucket_id)
```

## Additional Resources

- [AWS CLI S3 Commands](https://docs.aws.amazon.com/cli/latest/reference/s3/)
- [Fluent Bit S3 Output](https://docs.fluentbit.io/manual/pipeline/outputs/s3)
- [AWS SDK Documentation](https://aws.amazon.com/tools/)
