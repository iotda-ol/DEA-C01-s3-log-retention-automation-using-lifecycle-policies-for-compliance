# S3 Log Retention Automation using Lifecycle Policies

## Overview

This repository demonstrates an automated log retention solution using Amazon S3 Lifecycle policies. Server logs are stored in S3 and automatically deleted after one year to meet compliance requirements. The solution minimizes operational overhead and is implemented using Terraform following AWS DEA-C01 best practices.

## Architecture

```
┌─────────────────┐
│  Log Sources    │
│ (EC2/Lambda/ECS)│
└────────┬────────┘
         │
         │ Write Logs
         │ (Least-privilege IAM)
         ▼
┌─────────────────────────────────────────────────────┐
│           S3 Bucket (Encrypted)                     │
│  ┌───────────────────────────────────────────────┐  │
│  │  Lifecycle Policy (Automated)                 │  │
│  │  • Day 0-90:   STANDARD Storage               │  │
│  │  • Day 91-180: STANDARD_IA (Cost Optimization)│  │
│  │  • Day 181-365: GLACIER (Cost Optimization)   │  │
│  │  • Day 365+:   AUTO-DELETE (Compliance)       │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Features

### Security & Compliance
- ✅ **Encryption at Rest**: AES-256 or AWS KMS encryption enabled by default
- ✅ **Block Public Access**: All public access blocked at bucket level
- ✅ **Least-Privilege IAM**: Minimal permissions for log writing operations only
- ✅ **Versioning**: Optional versioning for data protection and audit trails
- ✅ **Compliance Tags**: Resource tagging for governance and compliance tracking

### Automated Lifecycle Management
- ✅ **1-Year Retention**: Automatic deletion after 365 days
- ✅ **Storage Class Transitions**: Automated cost optimization
- ✅ **Version Cleanup**: Automatic cleanup of old object versions
- ✅ **Multipart Upload Cleanup**: Automatic cleanup of incomplete uploads

### Cost Optimization
- ✅ **Tiered Storage**: Automatic transition to lower-cost storage classes
- ✅ **No Operational Overhead**: Fully automated with no manual intervention
- ✅ **Predictable Costs**: Clear cost structure based on retention policy

## Why S3 Lifecycle Policies? (DEA-C01 Best Practice)

### Lowest Operational Overhead

S3 Lifecycle policies provide the **lowest operational overhead** compared to alternative approaches:

#### Alternative Approaches (Higher Overhead)
1. **Lambda Functions + CloudWatch Events**
   - ❌ Requires custom code development and maintenance
   - ❌ Need to handle pagination for large buckets
   - ❌ Must manage Lambda execution errors and retries
   - ❌ Additional costs for Lambda executions and CloudWatch Events
   - ❌ Potential for missed deletions if Lambda fails

2. **AWS Step Functions**
   - ❌ Complex state machine design and maintenance
   - ❌ Higher costs per execution
   - ❌ Requires monitoring and error handling logic

3. **Manual Scripts/Cron Jobs**
   - ❌ Infrastructure to host and run scripts
   - ❌ Manual maintenance and updates required
   - ❌ Risk of script failures and missed executions
   - ❌ No built-in retry or error handling

#### S3 Lifecycle Policies (Lowest Overhead) ✅
- ✅ **Native AWS Service**: Built-in, fully managed by AWS
- ✅ **No Code Required**: Declarative configuration only
- ✅ **Zero Maintenance**: AWS handles all execution and retry logic
- ✅ **No Additional Costs**: Lifecycle transitions are free (only pay for storage)
- ✅ **Guaranteed Execution**: AWS ensures policy rules are applied
- ✅ **Audit Trail**: AWS CloudTrail logs all lifecycle actions
- ✅ **Scalable**: Handles millions of objects without performance issues
- ✅ **Infrastructure as Code**: Easily managed via Terraform

### DEA-C01 Alignment

This solution aligns with AWS Certified Data Engineer Associate (DEA-C01) best practices:

1. **Automated Data Lifecycle Management**
   - Uses native AWS services for automation
   - Reduces manual intervention and operational burden
   - Ensures consistent policy enforcement

2. **Cost Optimization**
   - Implements storage class transitions for cost savings
   - Eliminates unnecessary storage costs after retention period
   - No compute costs for deletion operations

3. **Compliance & Governance**
   - Enforces retention policies automatically
   - Provides audit trails via CloudTrail
   - Supports regulatory compliance (GDPR, HIPAA, SOC 2)

4. **Security Best Practices**
   - Encryption at rest (AES-256 or KMS)
   - Least-privilege IAM policies
   - Public access blocking

5. **Scalability & Reliability**
   - Handles any volume of logs without configuration changes
   - No single point of failure
   - AWS-managed service with high availability

## Compliance Benefits

### Regulatory Compliance

This solution helps meet various compliance requirements:

1. **Data Retention Policies**
   - Automatically enforces 1-year retention period
   - Ensures logs are retained for audit purposes
   - Guarantees deletion after retention period expires

2. **Data Privacy Regulations (GDPR, CCPA)**
   - Automatic deletion prevents indefinite data storage
   - Reduces risk of retaining personal data beyond necessary period
   - Demonstrates commitment to data minimization principles

3. **Industry Standards (PCI-DSS, HIPAA, SOC 2)**
   - Log retention for security monitoring and incident response
   - Audit trail of data lifecycle management
   - Encryption and access controls meet security requirements

4. **Cost Governance**
   - Predictable storage costs based on retention policy
   - Automatic cleanup prevents cost overruns
   - Resource tagging enables cost allocation and tracking

### Audit & Reporting

- **CloudTrail Integration**: All S3 lifecycle actions are logged
- **Compliance Reports**: Use AWS Config to verify lifecycle policies
- **Tag-Based Reporting**: Track costs and compliance by tags
- **Versioning**: Optional object versioning provides additional audit trail

## Cost Optimization Strategy

### Storage Class Transitions

The solution uses a multi-tier storage strategy to minimize costs:

1. **Day 0-90: STANDARD Storage**
   - Frequent access expected during this period
   - Fastest retrieval times for recent logs
   - Higher storage cost, but optimal for active logs

2. **Day 91-180: STANDARD_IA (Infrequent Access)**
   - 45% cost reduction compared to STANDARD
   - Logs accessed less frequently after 90 days
   - Millisecond retrieval times when needed

3. **Day 181-365: GLACIER Storage**
   - 85% cost reduction compared to STANDARD
   - Long-term archival before deletion
   - Suitable for compliance and rare access scenarios

4. **Day 365+: Automatic Deletion**
   - Zero storage cost after retention period
   - Ensures compliance with retention policies
   - No manual intervention required

### Cost Savings Example

For 1TB of logs per month with 1-year retention:

| Approach | Monthly Cost* | Annual Cost* | Operational Overhead |
|----------|--------------|--------------|---------------------|
| STANDARD only | $23.55 | $282.60 | Low |
| With Lifecycle (our solution) | $8.42 | $101.04 | **None** |
| Lambda-based deletion | $10.50 | $126.00 | High |

*Approximate costs based on US-East-1 pricing. Actual costs vary by region and usage patterns.

**Annual Savings**: ~$181 per TB with lifecycle transitions vs. STANDARD only

### Additional Cost Benefits

- **No Compute Costs**: Lifecycle transitions are free (no Lambda, Step Functions, etc.)
- **No Data Transfer Costs**: Internal AWS operations are free
- **Reduced Support Burden**: No custom code to maintain or troubleshoot
- **Predictable Costs**: Easy to forecast based on log volume and retention

## Deployment Instructions

### Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- AWS account with appropriate permissions
- AWS CLI configured with credentials

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance
   ```

2. **Configure variables**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your specific configuration
   nano terraform.tfvars
   ```

3. **Initialize Terraform**
   ```bash
   terraform init
   ```

4. **Review the execution plan**
   ```bash
   terraform plan
   ```

5. **Deploy the infrastructure**
   ```bash
   terraform apply
   ```

6. **Note the outputs**
   ```bash
   terraform output
   ```

### Configuration Options

Edit `terraform.tfvars` to customize:

- `bucket_name`: Globally unique S3 bucket name
- `retention_days`: Number of days to retain logs (default: 365)
- `transition_to_ia_days`: Days before moving to Infrequent Access (default: 90)
- `transition_to_glacier_days`: Days before moving to Glacier (default: 180)
- `enable_versioning`: Enable/disable object versioning
- `kms_key_id`: Optional KMS key for encryption
- `tags`: Resource tags for compliance and cost tracking

## IAM Configuration

### Using the IAM Role

The Terraform creates an IAM role that can be assumed by EC2, Lambda, or ECS tasks:

**For EC2 Instances:**
```bash
# Attach the instance profile to your EC2 instance
aws ec2 associate-iam-instance-profile \
  --instance-id i-1234567890abcdef0 \
  --iam-instance-profile Name=$(terraform output -raw log_writer_instance_profile_name)
```

**For Lambda Functions:**
```hcl
resource "aws_lambda_function" "example" {
  # ... other configuration ...
  role = aws_iam_role.log_writer_role.arn
}
```

**For ECS Tasks:**
```hcl
resource "aws_ecs_task_definition" "example" {
  # ... other configuration ...
  task_role_arn = aws_iam_role.log_writer_role.arn
}
```

### Least-Privilege Policy

The IAM policy grants only the minimum permissions required:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Resource": "arn:aws:s3:::bucket-name/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::bucket-name"
    }
  ]
}
```

## Writing Logs to S3

### Using AWS CLI
```bash
aws s3 cp application.log s3://$(terraform output -raw bucket_id)/logs/$(date +%Y/%m/%d)/
```

### Using AWS SDK (Python)
```python
import boto3
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = 'your-bucket-name'
log_file = 'application.log'
key = f"logs/{datetime.now().strftime('%Y/%m/%d')}/{log_file}"

s3.upload_file(log_file, bucket_name, key)
```

### Using Fluent Bit / Fluentd
```conf
[OUTPUT]
    Name s3
    Match *
    bucket your-bucket-name
    region us-east-1
    store_dir /tmp/fluent-bit-s3
    s3_key_format /logs/%Y/%m/%d/$UUID.log
```

## Monitoring & Validation

### Verify Lifecycle Policy
```bash
aws s3api get-bucket-lifecycle-configuration \
  --bucket $(terraform output -raw bucket_id)
```

### Check Bucket Encryption
```bash
aws s3api get-bucket-encryption \
  --bucket $(terraform output -raw bucket_id)
```

### View CloudTrail Logs
```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=$(terraform output -raw bucket_id) \
  --max-results 50
```

### Monitor with CloudWatch
- S3 Request Metrics: Track PUT operations
- S3 Storage Metrics: Monitor bucket size and object count
- CloudTrail Insights: Detect unusual API activity

## Cleanup

To destroy all resources:

```bash
# Note: Bucket must be empty before destruction
aws s3 rm s3://$(terraform output -raw bucket_id) --recursive

# Destroy infrastructure
terraform destroy
```

## Best Practices Checklist

- ✅ Encryption enabled (AES-256 or KMS)
- ✅ Public access blocked
- ✅ Lifecycle policy configured for 1-year retention
- ✅ Storage class transitions for cost optimization
- ✅ Least-privilege IAM policies
- ✅ Resource tagging for compliance
- ✅ Versioning enabled (optional)
- ✅ Access logging configured (optional)
- ✅ CloudTrail integration for audit trails
- ✅ Infrastructure as Code (Terraform)

## Troubleshooting

### Issue: Bucket name already exists
**Solution**: S3 bucket names are globally unique. Change `bucket_name` in `terraform.tfvars`

### Issue: Access denied when writing logs
**Solution**: Verify IAM role/policy is attached and has correct permissions

### Issue: Objects not being deleted after 365 days
**Solution**: 
- Check lifecycle policy is enabled: `aws s3api get-bucket-lifecycle-configuration`
- Lifecycle rules run daily, typically at midnight UTC
- Objects must be at least 365 days old (based on creation date)

### Issue: High storage costs
**Solution**: 
- Verify lifecycle transitions are working
- Check if objects are being deleted after retention period
- Review CloudWatch metrics for storage class distribution

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue in the GitHub repository
- Review AWS documentation for S3 Lifecycle policies
- Consult AWS Support for account-specific issues

## References

- [AWS S3 Lifecycle Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [DEA-C01 Exam Guide](https://aws.amazon.com/certification/certified-data-engineer-associate/)
- [S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
