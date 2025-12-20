# Steps 11-20: AWS Account Setup and Configuration

## Step 11: Setting Up AWS Billing Alerts

**Why Billing Alerts?**
Prevent unexpected costs by getting notified when spending exceeds thresholds.

**Enable Billing Alerts**:
1. Sign in to AWS Console as root user
2. Click your account name → "Account"
3. Scroll to "Billing preferences"
4. Check "Receive Billing Alerts"
5. Save preferences

**Create Budget Alert**:
```bash
# Using AWS CLI
aws budgets create-budget \
    --account-id $(aws sts get-caller-identity --query Account --output text) \
    --budget file://budget.json \
    --notifications-with-subscribers file://notifications.json
```

**budget.json**:
```json
{
  "BudgetName": "S3-Log-Retention-Monthly",
  "BudgetLimit": {
    "Amount": "10",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST",
  "CostFilters": {
    "Service": ["Amazon Simple Storage Service"]
  }
}
```

**notifications.json**:
```json
[
  {
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80,
      "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [
      {
        "SubscriptionType": "EMAIL",
        "Address": "your-email@example.com"
      }
    ]
  }
]
```

---

## Step 12: IAM Best Practices and Security

**Principle of Least Privilege**:
Grant only the permissions needed to perform specific tasks.

**Create Custom IAM Policy for S3 Log Management**:

**s3-log-retention-policy.json**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3BucketManagement",
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:GetBucketVersioning",
        "s3:PutBucketVersioning"
      ],
      "Resource": "arn:aws:s3:::*log*"
    },
    {
      "Sid": "S3LifecycleManagement",
      "Effect": "Allow",
      "Action": [
        "s3:GetLifecycleConfiguration",
        "s3:PutLifecycleConfiguration"
      ],
      "Resource": "arn:aws:s3:::*log*"
    },
    {
      "Sid": "S3ObjectManagement",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::*log*/*"
    },
    {
      "Sid": "CloudWatchMonitoring",
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricAlarm",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:DescribeAlarms"
      ],
      "Resource": "*"
    }
  ]
}
```

**Apply Policy**:
```bash
# Create policy
aws iam create-policy \
    --policy-name S3LogRetentionPolicy \
    --policy-document file://s3-log-retention-policy.json

# Attach to user
aws iam attach-user-policy \
    --user-name log-retention-admin \
    --policy-arn arn:aws:iam::ACCOUNT_ID:policy/S3LogRetentionPolicy
```

**Enable MFA**:
1. IAM Console → Users → Your User
2. Security credentials tab
3. Assigned MFA device → Manage
4. Choose "Virtual MFA device"
5. Scan QR code with authenticator app (Google Authenticator, Authy)
6. Enter two consecutive MFA codes

---

## Step 13: Setting Up CloudTrail for Audit Logs

**Why CloudTrail?**
- Records all API calls in your account
- Provides audit trail for compliance
- Helps detect security issues
- Integrates with CloudWatch

**Create CloudTrail**:
```bash
# Create S3 bucket for CloudTrail logs
TRAIL_BUCKET="cloudtrail-logs-$(aws sts get-caller-identity --query Account --output text)"
aws s3 mb s3://$TRAIL_BUCKET

# Apply bucket policy for CloudTrail
cat > trail-bucket-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCloudTrailAclCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::$TRAIL_BUCKET"
    },
    {
      "Sid": "AWSCloudTrailWrite",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::$TRAIL_BUCKET/AWSLogs/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    }
  ]
}
EOF

aws s3api put-bucket-policy \
    --bucket $TRAIL_BUCKET \
    --policy file://trail-bucket-policy.json

# Create trail
aws cloudtrail create-trail \
    --name s3-log-retention-trail \
    --s3-bucket-name $TRAIL_BUCKET \
    --is-multi-region-trail

# Start logging
aws cloudtrail start-logging \
    --name s3-log-retention-trail
```

---

## Step 14: Understanding VPC and Networking (Optional)

**VPC Endpoints for S3**:
Access S3 without internet gateway (improves security and reduces costs).

**Benefits**:
- Traffic stays within AWS network
- No data transfer charges for S3
- Enhanced security
- Better performance

**Create VPC Endpoint**:
```bash
# Get VPC ID
VPC_ID=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId' --output text)

# Get route table IDs
ROUTE_TABLE_IDS=$(aws ec2 describe-route-tables \
    --filters "Name=vpc-id,Values=$VPC_ID" \
    --query 'RouteTables[*].RouteTableId' \
    --output text)

# Create S3 VPC endpoint
aws ec2 create-vpc-endpoint \
    --vpc-id $VPC_ID \
    --service-name com.amazonaws.us-east-1.s3 \
    --route-table-ids $ROUTE_TABLE_IDS
```

---

## Step 15: Setting Up AWS Cost Explorer

**Enable Cost Explorer**:
1. AWS Console → Billing and Cost Management
2. Cost Explorer
3. Enable Cost Explorer (takes 24 hours to populate data)

**Using Cost Explorer**:
- View costs by service
- Filter by tags
- Create custom reports
- Set up savings plans

**Cost Allocation Tags**:
```bash
# Tag S3 bucket
aws s3api put-bucket-tagging \
    --bucket my-log-bucket \
    --tagging 'TagSet=[
        {Key=Project,Value=LogRetention},
        {Key=Environment,Value=Production},
        {Key=CostCenter,Value=Engineering}
    ]'

# Activate cost allocation tags in console
# Billing → Cost Allocation Tags → Select tags → Activate
```

---

## Step 16: AWS Organizations and Multi-Account Setup

**Why Multiple Accounts?**
- Isolate environments (dev, staging, prod)
- Separate billing
- Enhanced security
- Blast radius containment

**Create Organization** (if managing multiple accounts):
```bash
# Create organization
aws organizations create-organization

# Create accounts
aws organizations create-account \
    --email dev@example.com \
    --account-name "Log Retention - Dev"

aws organizations create-account \
    --email prod@example.com \
    --account-name "Log Retention - Prod"
```

**Cross-Account Access**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::CENTRAL_ACCOUNT:root"
      },
      "Action": "sts:AssumeRole",
      "Resource": "*"
    }
  ]
}
```

---

## Step 17: Setting Up AWS Config for Compliance

**Why AWS Config?**
- Track resource configuration changes
- Ensure compliance with rules
- Historical configuration tracking
- Integration with other AWS services

**Enable AWS Config**:
```bash
# Create Config bucket
CONFIG_BUCKET="aws-config-$(aws sts get-caller-identity --query Account --output text)"
aws s3 mb s3://$CONFIG_BUCKET

# Create IAM role for Config
aws iam create-role \
    --role-name AWSConfigRole \
    --assume-role-policy-document file://config-trust-policy.json

aws iam attach-role-policy \
    --role-name AWSConfigRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/ConfigRole

# Start configuration recorder
aws configservice put-configuration-recorder \
    --configuration-recorder name=default,roleARN=arn:aws:iam::ACCOUNT_ID:role/AWSConfigRole

# Set up delivery channel
aws configservice put-delivery-channel \
    --delivery-channel name=default,s3BucketName=$CONFIG_BUCKET
```

**Config Rules for S3**:
- s3-bucket-versioning-enabled
- s3-bucket-public-read-prohibited
- s3-bucket-public-write-prohibited
- s3-bucket-ssl-requests-only
- s3-bucket-server-side-encryption-enabled

---

## Step 18: Understanding Regions and Availability Zones

**AWS Global Infrastructure**:
- **Regions**: Geographic locations (e.g., us-east-1, eu-west-1)
- **Availability Zones**: Isolated data centers within a region
- **Edge Locations**: CDN endpoints for CloudFront

**Choosing a Region**:
Factors to consider:
1. **Latency**: Proximity to users
2. **Compliance**: Data residency requirements
3. **Cost**: Pricing varies by region
4. **Services**: Not all services available in all regions

**List Available Regions**:
```bash
# List all regions
aws ec2 describe-regions --output table

# List regions where S3 is available (all regions)
aws ec2 describe-regions \
    --query 'Regions[*].RegionName' \
    --output text
```

**Multi-Region Strategy**:
- Primary region: us-east-1 (lowest cost, all services)
- DR region: us-west-2 (different coast)
- EU region: eu-west-1 (GDPR compliance)

---

## Step 19: Setting Up AWS Systems Manager Parameter Store

**Why Parameter Store?**
- Secure storage for configuration
- Centralized management
- Version control
- Integration with other AWS services
- Free (standard parameters)

**Store Configuration**:
```bash
# Store S3 bucket name
aws ssm put-parameter \
    --name /log-retention/bucket-name \
    --value "my-log-bucket" \
    --type String \
    --description "S3 bucket for log storage"

# Store retention period
aws ssm put-parameter \
    --name /log-retention/retention-days \
    --value "365" \
    --type String \
    --description "Log retention period in days"

# Store encrypted value
aws ssm put-parameter \
    --name /log-retention/api-key \
    --value "secret-api-key" \
    --type SecureString \
    --description "API key for log ingestion"

# Retrieve parameter
aws ssm get-parameter \
    --name /log-retention/bucket-name \
    --query 'Parameter.Value' \
    --output text
```

**Python Integration**:
```python
import boto3

ssm = boto3.client('ssm')

# Get parameter
response = ssm.get_parameter(Name='/log-retention/bucket-name')
bucket_name = response['Parameter']['Value']

# Get encrypted parameter
response = ssm.get_parameter(
    Name='/log-retention/api-key',
    WithDecryption=True
)
api_key = response['Parameter']['Value']
```

---

## Step 20: Documentation and Tagging Standards

**Tagging Strategy**:
Consistent tagging is crucial for:
- Cost allocation
- Resource organization
- Automation
- Compliance reporting

**Recommended Tags**:
```yaml
Required Tags:
  - Environment: [dev, staging, prod]
  - Project: log-retention
  - Owner: platform-team
  - CostCenter: engineering
  - ManagedBy: terraform

Optional Tags:
  - Application: web-server
  - Compliance: dea-c01
  - DataClassification: [public, internal, confidential]
  - BackupSchedule: daily
  - RetentionPeriod: 365d
```

**Apply Tags with Terraform**:
```hcl
locals {
  common_tags = {
    Project     = "log-retention"
    Environment = var.environment
    ManagedBy   = "terraform"
    Compliance  = "DEA-C01"
    Owner       = "platform-team"
  }
}

resource "aws_s3_bucket" "logs" {
  bucket = var.bucket_name
  tags   = merge(local.common_tags, var.additional_tags)
}
```

**Tag Governance**:
```bash
# List untagged resources
aws resourcegroupstaggingapi get-resources \
    --resource-type-filters s3:bucket \
    --query 'ResourceTagMappingList[?Tags==`[]`].ResourceARN'

# Enforce tagging with AWS Config rule
aws configservice put-config-rule \
    --config-rule file://required-tags-rule.json
```

**Documentation Standards**:
1. **README.md**: Project overview and quick start
2. **ARCHITECTURE.md**: System design and components
3. **RUNBOOK.md**: Operational procedures
4. **TROUBLESHOOTING.md**: Common issues and solutions
5. **CHANGELOG.md**: Version history

---

## Summary of Steps 11-20

**What You've Learned**:
✅ Billing alerts and cost monitoring
✅ IAM security best practices
✅ CloudTrail for audit logging
✅ VPC endpoints for S3
✅ Cost Explorer and optimization
✅ Multi-account strategies
✅ AWS Config for compliance
✅ Regional considerations
✅ Parameter Store for configuration
✅ Tagging and documentation standards

**Next Steps** (Steps 21-30):
- Deep dive into S3 bucket configuration
- Object lifecycle management
- Storage class details
- Performance optimization
- Security hardening

**Checklist**:
- [ ] Billing alerts configured
- [ ] IAM policies created and tested
- [ ] CloudTrail enabled and logging
- [ ] Cost allocation tags activated
- [ ] Parameter Store configured
- [ ] Tagging strategy documented
- [ ] VPC endpoints created (if applicable)
- [ ] Multi-account strategy defined
- [ ] AWS Config rules enabled
- [ ] Documentation created
