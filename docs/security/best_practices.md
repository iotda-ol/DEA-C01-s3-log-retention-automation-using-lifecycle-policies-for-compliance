# Security Best Practices

Security guidelines for S3 log retention automation.

## Infrastructure Security

### S3 Bucket Security

**Enable Encryption**
```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"  # or "aws:kms"
    }
  }
}
```

**Block Public Access**
```hcl
resource "aws_s3_bucket_public_access_block" "logs" {
  bucket = aws_s3_bucket.logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

**Enable Versioning**
```hcl
resource "aws_s3_bucket_versioning" "logs" {
  bucket = aws_s3_bucket.logs.id
  
  versioning_configuration {
    status = "Enabled"
  }
}
```

### IAM Security

**Least Privilege Principle**

Grant minimum required permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::log-bucket",
        "arn:aws:s3:::log-bucket/*"
      ]
    }
  ]
}
```

**Use Roles Instead of Keys**

For EC2, Lambda, ECS:
```hcl
resource "aws_iam_role" "log_processor" {
  name = "log-processor-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}
```

**Enable MFA Delete**

For critical buckets:
```bash
aws s3api put-bucket-versioning \
  --bucket log-bucket \
  --versioning-configuration Status=Enabled,MFADelete=Enabled \
  --mfa "device-serial-number mfa-code"
```

## Application Security

### Secrets Management

**Never commit secrets**

Use environment variables or AWS Secrets Manager:

```python
import boto3
import os

# Good: Use environment variables
access_key = os.getenv('AWS_ACCESS_KEY_ID')

# Better: Use IAM roles
s3_client = boto3.client('s3')  # Uses IAM role automatically
```

**Use AWS Secrets Manager**

```python
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']
```

### Input Validation

**Validate all inputs**

```python
from pydantic import BaseModel, validator

class LogUploadRequest(BaseModel):
    bucket_name: str
    key: str
    
    @validator('bucket_name')
    def validate_bucket_name(cls, v):
        if not v.replace('-', '').replace('.', '').isalnum():
            raise ValueError('Invalid bucket name')
        return v
```

### Secure Logging

**Don't log sensitive data**

```python
import logging

logger = logging.getLogger(__name__)

# Bad
logger.info(f"Processing user: {user_email}")

# Good
logger.info(f"Processing user: {hash(user_email)}")
```

## Network Security

### VPC Endpoints

Use VPC endpoints for S3:

```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.region}.s3"
  
  route_table_ids = var.route_table_ids
}
```

### Bucket Policies

Restrict access by VPC:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::log-bucket",
        "arn:aws:s3:::log-bucket/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:SourceVpc": "vpc-12345678"
        }
      }
    }
  ]
}
```

## Monitoring and Auditing

### CloudTrail

Enable CloudTrail for API logging:

```hcl
resource "aws_cloudtrail" "logs" {
  name                          = "log-bucket-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_logging                = true
}
```

### S3 Access Logging

Enable bucket access logs:

```hcl
resource "aws_s3_bucket_logging" "logs" {
  bucket = aws_s3_bucket.logs.id

  target_bucket = aws_s3_bucket.access_logs.id
  target_prefix = "log-access/"
}
```

### CloudWatch Alarms

Monitor suspicious activity:

```hcl
resource "aws_cloudwatch_metric_alarm" "unauthorized_api_calls" {
  alarm_name          = "s3-unauthorized-api-calls"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "UnauthorizedAPICalls"
  namespace           = "AWS/S3"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

## Compliance

### Data Retention

Document retention policies:

| Log Type | Retention | Reason |
|----------|-----------|--------|
| Access   | 1 year    | SOC2 requirement |
| Application | 90 days | Operational need |
| Audit    | 7 years   | HIPAA requirement |

### Encryption Standards

- Use AES-256 minimum
- Rotate keys annually
- Use AWS KMS for sensitive data

### Access Control

- Review IAM policies quarterly
- Use groups, not individual users
- Enable MFA for privileged accounts

## Incident Response

### Detect

- Monitor CloudTrail logs
- Set up CloudWatch alarms
- Use GuardDuty

### Respond

1. Isolate affected resources
2. Review access logs
3. Rotate credentials
4. Document findings

### Recover

1. Restore from backups
2. Apply security patches
3. Update policies
4. Conduct post-mortem

## Security Checklist

- [ ] Encryption at rest enabled
- [ ] Encryption in transit enforced
- [ ] Public access blocked
- [ ] Versioning enabled
- [ ] MFA delete configured
- [ ] Least privilege IAM policies
- [ ] CloudTrail logging enabled
- [ ] S3 access logging enabled
- [ ] VPC endpoints configured
- [ ] Secrets in Secrets Manager
- [ ] Input validation implemented
- [ ] Security monitoring active
- [ ] Incident response plan documented

## Tools and Scanning

### Static Analysis

```bash
# Terraform security scan
tfsec terraform/

# Python security scan
bandit -r src/

# Dependency vulnerability scan
pip-audit
```

### Dynamic Analysis

```bash
# AWS Config rules
aws configservice describe-config-rules

# AWS Security Hub
aws securityhub get-findings
```

## References

- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [S3 Security](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
