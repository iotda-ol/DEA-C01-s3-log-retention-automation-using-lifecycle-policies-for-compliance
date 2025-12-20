# S3 Log Retention Automation - Complete 100-Step Guide
## From Novice to Expert

This comprehensive guide takes you through the complete process of implementing and mastering AWS S3 log retention automation using lifecycle policies, from basic concepts to advanced enterprise implementations.

---

## Table of Contents
1. [Beginner Level (Steps 1-25)](#beginner-level)
2. [Intermediate Level (Steps 26-50)](#intermediate-level)
3. [Advanced Level (Steps 51-75)](#advanced-level)
4. [Expert Level (Steps 76-100)](#expert-level)

---

## Beginner Level

### Prerequisites & Setup (Steps 1-10)

#### Step 1: Understand AWS S3 Basics
- Learn what Amazon S3 is and its purpose
- Understand buckets, objects, and keys
- Review S3 storage classes
- **Resource**: [AWS S3 Documentation](https://aws.amazon.com/s3/)

#### Step 2: Set Up AWS Account
- Create an AWS account if you don't have one
- Enable MFA for root account security
- Create an IAM user for development
- **Verification**: Login to AWS Console

#### Step 3: Install AWS CLI
```bash
# For Linux/Mac
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

#### Step 4: Configure AWS CLI
```bash
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Enter default region (e.g., us-east-1)
# Enter output format (json recommended)
```

#### Step 5: Install Python
```bash
# Check Python version (3.8+ required)
python3 --version

# Install pip if not available
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

#### Step 6: Install Terraform
```bash
# Download Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform --version
```

#### Step 7: Clone the Repository
```bash
git clone https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance
```

#### Step 8: Understand Project Structure
- Review the `README.md` file
- Explore the folder structure
- Understand the purpose of each directory
- **Action**: Run `tree -L 2` to visualize structure

#### Step 9: Install Python Dependencies
```bash
cd python
pip install -r requirements.txt
```

#### Step 10: Understand Lifecycle Policies
- Learn what S3 lifecycle policies are
- Understand transitions and expirations
- Review compliance requirements
- **Resource**: Read `docs/beginner/01-lifecycle-basics.md`

### Basic Concepts (Steps 11-25)

#### Step 11: Review S3 Storage Classes
- Understand Standard, IA, Glacier, and Deep Archive
- Learn cost implications
- Review retrieval times
- **Exercise**: Compare storage class pricing

#### Step 12: Understand Compliance Requirements
- Learn about data retention regulations
- Understand 1-year retention requirement
- Review audit requirements
- **Document**: Review compliance checklist

#### Step 13: Create Your First S3 Bucket (Manual)
```bash
aws s3 mb s3://my-log-bucket-test-$(date +%s)
```

#### Step 14: Upload Test Log Files
```bash
echo "Test log entry" > test.log
aws s3 cp test.log s3://my-log-bucket-test-*/
```

#### Step 15: List S3 Bucket Contents
```bash
aws s3 ls s3://my-log-bucket-test-*/
```

#### Step 16: Understand Terraform Basics
- Learn HCL syntax
- Understand resources and providers
- Review state management
- **Tutorial**: Complete Terraform getting started guide

#### Step 17: Review S3 Terraform Resource
```hcl
# Example S3 bucket in Terraform
resource "aws_s3_bucket" "log_bucket" {
  bucket = "my-log-bucket"
  
  tags = {
    Purpose = "Log Storage"
  }
}
```

#### Step 18: Understand Lifecycle Configuration Structure
```json
{
  "Rules": [{
    "Id": "Delete old logs",
    "Status": "Enabled",
    "Expiration": {
      "Days": 365
    }
  }]
}
```

#### Step 19: Apply Simple Lifecycle Policy (Manual)
```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-log-bucket-test-* \
  --lifecycle-configuration file://simple-lifecycle.json
```

#### Step 20: Verify Lifecycle Policy
```bash
aws s3api get-bucket-lifecycle-configuration \
  --bucket my-log-bucket-test-*
```

#### Step 21: Understand Python Boto3 Basics
```python
import boto3

# Create S3 client
s3 = boto3.client('s3')

# List buckets
response = s3.list_buckets()
print(response)
```

#### Step 22: Create Python Script to List Buckets
- Write a simple script using boto3
- Handle exceptions
- Print results
- **File**: `examples/basic/list_buckets.py`

#### Step 23: Understand IAM Roles and Policies
- Learn about least privilege principle
- Review S3 permissions
- Understand policy structure
- **Resource**: AWS IAM documentation

#### Step 24: Create IAM Policy for S3 Access
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:*"],
    "Resource": ["arn:aws:s3:::my-log-bucket/*"]
  }]
}
```

#### Step 25: Review Security Best Practices
- Enable bucket versioning
- Enable encryption at rest
- Use SSL for data in transit
- Review bucket policies
- **Checklist**: Security review completed ✓

---

## Intermediate Level

### Terraform Implementation (Steps 26-40)

#### Step 26: Initialize Terraform Project
```bash
cd terraform/environments/dev
terraform init
```

#### Step 27: Review Terraform Provider Configuration
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

#### Step 28: Create S3 Bucket Module
- Navigate to `terraform/modules/s3-bucket`
- Create `main.tf`, `variables.tf`, `outputs.tf`
- Implement bucket resource with best practices
- **Module**: S3 bucket module created

#### Step 29: Add Bucket Versioning
```hcl
resource "aws_s3_bucket_versioning" "log_bucket" {
  bucket = aws_s3_bucket.log_bucket.id
  
  versioning_configuration {
    status = "Enabled"
  }
}
```

#### Step 30: Add Server-Side Encryption
```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "log_bucket" {
  bucket = aws_s3_bucket.log_bucket.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

#### Step 31: Create Lifecycle Policy Module
- Navigate to `terraform/modules/lifecycle-policy`
- Implement lifecycle rules
- Add transition and expiration rules
- **Module**: Lifecycle policy module created

#### Step 32: Implement 1-Year Retention Policy
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "log_retention" {
  bucket = var.bucket_id
  
  rule {
    id     = "delete-old-logs"
    status = "Enabled"
    
    expiration {
      days = 365
    }
  }
}
```

#### Step 33: Add Transition Rules for Cost Optimization
```hcl
rule {
  id     = "transition-to-glacier"
  status = "Enabled"
  
  transition {
    days          = 90
    storage_class = "GLACIER"
  }
  
  expiration {
    days = 365
  }
}
```

#### Step 34: Create IAM Module
- Navigate to `terraform/modules/iam`
- Create roles for S3 access
- Implement least privilege policies
- **Module**: IAM module created

#### Step 35: Implement S3 Access Role
```hcl
resource "aws_iam_role" "s3_log_access" {
  name = "s3-log-access-role"
  
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

#### Step 36: Create Terraform Variables File
```hcl
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "retention_days" {
  description = "Number of days to retain logs"
  type        = number
  default     = 365
}
```

#### Step 37: Create Terraform Outputs
```hcl
output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = module.s3_bucket.bucket_name
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = module.s3_bucket.bucket_arn
}
```

#### Step 38: Validate Terraform Configuration
```bash
cd terraform/environments/dev
terraform validate
```

#### Step 39: Plan Terraform Deployment
```bash
terraform plan -out=tfplan
```

#### Step 40: Apply Terraform Configuration
```bash
terraform apply tfplan
```

### Python Automation (Steps 41-50)

#### Step 41: Create S3 Operations Module
- Navigate to `python/src/s3_operations`
- Create `__init__.py` and `client.py`
- Implement S3 client wrapper
- **Module**: S3 operations module created

#### Step 42: Implement Bucket Operations Class
```python
import boto3
from typing import List, Dict

class S3Operations:
    def __init__(self, region: str = 'us-east-1'):
        self.client = boto3.client('s3', region_name=region)
    
    def list_buckets(self) -> List[Dict]:
        """List all S3 buckets"""
        response = self.client.list_buckets()
        return response.get('Buckets', [])
```

#### Step 43: Add Upload Functionality
```python
def upload_file(self, file_path: str, bucket: str, key: str) -> bool:
    """Upload file to S3 bucket"""
    try:
        self.client.upload_file(file_path, bucket, key)
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False
```

#### Step 44: Create Lifecycle Management Module
- Navigate to `python/src/lifecycle_management`
- Create policy manager class
- Implement CRUD operations for lifecycle policies
- **Module**: Lifecycle management module created

#### Step 45: Implement Lifecycle Policy Getter
```python
class LifecycleManager:
    def __init__(self, s3_client):
        self.s3 = s3_client
    
    def get_lifecycle_policy(self, bucket: str) -> Dict:
        """Get lifecycle configuration for bucket"""
        try:
            response = self.s3.get_bucket_lifecycle_configuration(Bucket=bucket)
            return response
        except Exception as e:
            return {}
```

#### Step 46: Implement Lifecycle Policy Setter
```python
def set_lifecycle_policy(self, bucket: str, rules: List[Dict]) -> bool:
    """Set lifecycle configuration for bucket"""
    try:
        self.s3.put_bucket_lifecycle_configuration(
            Bucket=bucket,
            LifecycleConfiguration={'Rules': rules}
        )
        return True
    except Exception as e:
        print(f"Error setting lifecycle policy: {e}")
        return False
```

#### Step 47: Create Compliance Validation Module
- Navigate to `python/src/compliance`
- Create validator class
- Implement compliance checks
- **Module**: Compliance module created

#### Step 48: Implement Compliance Checker
```python
class ComplianceValidator:
    def __init__(self, required_retention_days: int = 365):
        self.required_retention_days = required_retention_days
    
    def validate_lifecycle_policy(self, policy: Dict) -> bool:
        """Validate lifecycle policy meets compliance requirements"""
        for rule in policy.get('Rules', []):
            if 'Expiration' in rule:
                days = rule['Expiration'].get('Days', 0)
                if days >= self.required_retention_days:
                    return True
        return False
```

#### Step 49: Create Configuration Management Module
```python
import json
import os

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
```

#### Step 50: Create Main Application Entry Point
```python
#!/usr/bin/env python3
"""Main application entry point for S3 log retention automation"""

import argparse
from src.s3_operations.client import S3Operations
from src.lifecycle_management.manager import LifecycleManager

def main():
    parser = argparse.ArgumentParser(
        description='S3 Log Retention Automation'
    )
    parser.add_argument('--bucket', required=True, help='S3 bucket name')
    parser.add_argument('--action', required=True, 
                       choices=['check', 'apply', 'validate'])
    
    args = parser.parse_args()
    
    # Initialize components
    s3_ops = S3Operations()
    lifecycle_mgr = LifecycleManager(s3_ops.client)
    
    if args.action == 'check':
        policy = lifecycle_mgr.get_lifecycle_policy(args.bucket)
        print(f"Current policy: {policy}")

if __name__ == '__main__':
    main()
```

---

## Advanced Level

### Advanced Terraform Patterns (Steps 51-65)

#### Step 51: Implement Terraform Remote State
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "s3-log-retention/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock-table"
  }
}
```

#### Step 52: Create State Bucket and Lock Table
```bash
# Create S3 bucket for state
aws s3 mb s3://terraform-state-bucket-$(aws sts get-caller-identity --query Account --output text)

# Create DynamoDB table for locking
aws dynamodb create-table \
  --table-name terraform-lock-table \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

#### Step 53: Implement Multi-Environment Strategy
- Create separate tfvars files for dev, staging, prod
- Use workspaces or separate state files
- Implement environment-specific configurations
- **Pattern**: Multi-environment setup complete

#### Step 54: Create Environment-Specific Variables
```hcl
# terraform/environments/dev/terraform.tfvars
environment      = "dev"
retention_days   = 365
bucket_prefix    = "dev-logs"
enable_glacier   = false

# terraform/environments/prod/terraform.tfvars
environment      = "prod"
retention_days   = 365
bucket_prefix    = "prod-logs"
enable_glacier   = true
glacier_days     = 90
```

#### Step 55: Implement CloudWatch Monitoring Module
```hcl
resource "aws_cloudwatch_metric_alarm" "s3_requests" {
  alarm_name          = "s3-high-request-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "AllRequests"
  namespace           = "AWS/S3"
  period              = "300"
  statistic           = "Sum"
  threshold           = "1000"
  
  dimensions = {
    BucketName = var.bucket_name
  }
}
```

#### Step 56: Add SNS Notifications for Lifecycle Events
```hcl
resource "aws_sns_topic" "s3_lifecycle_notifications" {
  name = "s3-lifecycle-notifications"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.log_bucket.id
  
  topic {
    topic_arn     = aws_sns_topic.s3_lifecycle_notifications.arn
    events        = ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
    filter_prefix = "logs/"
  }
}
```

#### Step 57: Implement Bucket Replication for DR
```hcl
resource "aws_s3_bucket_replication_configuration" "replication" {
  role   = aws_iam_role.replication.arn
  bucket = aws_s3_bucket.log_bucket.id
  
  rule {
    id     = "replicate-logs"
    status = "Enabled"
    
    destination {
      bucket        = aws_s3_bucket.replica_bucket.arn
      storage_class = "STANDARD_IA"
    }
  }
}
```

#### Step 58: Add Bucket Logging
```hcl
resource "aws_s3_bucket_logging" "log_bucket_logging" {
  bucket = aws_s3_bucket.log_bucket.id
  
  target_bucket = aws_s3_bucket.access_logs.id
  target_prefix = "log-bucket-access/"
}
```

#### Step 59: Implement Bucket Policy for Compliance
```hcl
resource "aws_s3_bucket_policy" "log_bucket_policy" {
  bucket = aws_s3_bucket.log_bucket.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyUnencryptedObjectUploads"
        Effect = "Deny"
        Principal = "*"
        Action = "s3:PutObject"
        Resource = "${aws_s3_bucket.log_bucket.arn}/*"
        Condition = {
          StringNotEquals = {
            "s3:x-amz-server-side-encryption": "AES256"
          }
        }
      }
    ]
  })
}
```

#### Step 60: Create Terraform Module Registry Structure
```
terraform/modules/
├── s3-bucket/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
├── lifecycle-policy/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── iam/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

#### Step 61: Implement Module Composition
```hcl
module "log_storage" {
  source = "../../modules/s3-bucket"
  
  bucket_name = "company-logs-${var.environment}"
  environment = var.environment
  
  versioning_enabled = true
  encryption_enabled = true
}

module "log_lifecycle" {
  source = "../../modules/lifecycle-policy"
  
  bucket_id       = module.log_storage.bucket_id
  retention_days  = var.retention_days
  glacier_enabled = var.enable_glacier
  glacier_days    = var.glacier_days
}
```

#### Step 62: Add Terraform Validation Tests
```bash
# Create validation script
cat > terraform/validate.sh << 'EOF'
#!/bin/bash
set -e

for dir in modules/*/; do
  echo "Validating $dir..."
  cd "$dir"
  terraform init -backend=false
  terraform validate
  cd -
done
EOF

chmod +x terraform/validate.sh
```

#### Step 63: Implement Terraform Documentation Generation
```bash
# Install terraform-docs
terraform-docs --version

# Generate documentation for each module
for module in terraform/modules/*/; do
  terraform-docs markdown "$module" > "$module/README.md"
done
```

#### Step 64: Create Terraform Cost Estimation
```bash
# Using Infracost
infracost breakdown --path terraform/environments/prod
```

#### Step 65: Implement Terraform Security Scanning
```bash
# Using tfsec
tfsec terraform/
```

### Advanced Python Implementation (Steps 66-75)

#### Step 66: Implement Async S3 Operations
```python
import asyncio
import aioboto3

class AsyncS3Operations:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
    
    async def upload_files(self, files: List[str], bucket: str):
        """Upload multiple files concurrently"""
        session = aioboto3.Session()
        async with session.client('s3', region_name=self.region) as s3:
            tasks = [
                s3.upload_file(file, bucket, os.path.basename(file))
                for file in files
            ]
            await asyncio.gather(*tasks)
```

#### Step 67: Implement Logging Framework
```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_level: str = 'INFO'):
    """Configure application logging"""
    logger = logging.getLogger('s3_log_retention')
    logger.setLevel(getattr(logging, log_level))
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(ch)
    
    # File handler
    fh = RotatingFileHandler(
        'logs/app.log', maxBytes=10485760, backupCount=5
    )
    fh.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(fh)
    
    return logger
```

#### Step 68: Create Monitoring and Metrics Module
```python
from prometheus_client import Counter, Histogram, start_http_server
import time

class MetricsCollector:
    def __init__(self):
        self.upload_counter = Counter(
            's3_uploads_total', 'Total S3 uploads'
        )
        self.upload_duration = Histogram(
            's3_upload_duration_seconds', 'S3 upload duration'
        )
    
    def record_upload(self, duration: float):
        """Record upload metrics"""
        self.upload_counter.inc()
        self.upload_duration.observe(duration)
```

#### Step 69: Implement Retry Logic with Exponential Backoff
```python
import time
from functools import wraps

def retry_with_backoff(retries=3, backoff_factor=2):
    """Decorator for retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator
```

#### Step 70: Create Database Integration for Audit Logging
```python
import sqlite3
from datetime import datetime

class AuditLogger:
    def __init__(self, db_path: str = 'audit.db'):
        self.conn = sqlite3.connect(db_path)
        self._create_table()
    
    def _create_table(self):
        """Create audit log table"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                bucket TEXT,
                object_key TEXT,
                user TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()
    
    def log_action(self, action: str, bucket: str, 
                   object_key: str, user: str, status: str):
        """Log an action to the audit database"""
        self.conn.execute('''
            INSERT INTO audit_logs 
            (timestamp, action, bucket, object_key, user, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), action, bucket, 
              object_key, user, status))
        self.conn.commit()
```

#### Step 71: Implement Policy Validation Framework
```python
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class ValidationRule:
    name: str
    check: callable
    error_message: str

class PolicyValidator:
    def __init__(self):
        self.rules: List[ValidationRule] = []
    
    def add_rule(self, rule: ValidationRule):
        """Add validation rule"""
        self.rules.append(rule)
    
    def validate(self, policy: Dict) -> Tuple[bool, List[str]]:
        """Validate policy against all rules"""
        errors = []
        for rule in self.rules:
            if not rule.check(policy):
                errors.append(rule.error_message)
        return len(errors) == 0, errors
```

#### Step 72: Create CLI with Rich Output
```python
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

def display_buckets(buckets: List[Dict]):
    """Display buckets in a formatted table"""
    table = Table(title="S3 Buckets")
    
    table.add_column("Name", style="cyan")
    table.add_column("Creation Date", style="magenta")
    table.add_column("Region", style="green")
    
    for bucket in buckets:
        table.add_row(
            bucket['Name'],
            bucket['CreationDate'].strftime('%Y-%m-%d'),
            bucket.get('Region', 'N/A')
        )
    
    console.print(table)
```

#### Step 73: Implement Configuration Schema Validation
```python
from jsonschema import validate, ValidationError

LIFECYCLE_POLICY_SCHEMA = {
    "type": "object",
    "properties": {
        "Rules": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Id": {"type": "string"},
                    "Status": {"enum": ["Enabled", "Disabled"]},
                    "Expiration": {
                        "type": "object",
                        "properties": {
                            "Days": {"type": "integer", "minimum": 1}
                        }
                    }
                },
                "required": ["Id", "Status"]
            }
        }
    },
    "required": ["Rules"]
}

def validate_lifecycle_policy(policy: Dict) -> bool:
    """Validate lifecycle policy against schema"""
    try:
        validate(instance=policy, schema=LIFECYCLE_POLICY_SCHEMA)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False
```

#### Step 74: Create Report Generation Module
```python
from jinja2 import Template
import json

class ReportGenerator:
    def __init__(self, template_path: str):
        with open(template_path, 'r') as f:
            self.template = Template(f.read())
    
    def generate_compliance_report(self, data: Dict) -> str:
        """Generate compliance report"""
        return self.template.render(
            buckets=data.get('buckets', []),
            policies=data.get('policies', []),
            compliance_status=data.get('compliance_status', {}),
            timestamp=datetime.now().isoformat()
        )
```

#### Step 75: Implement Integration Tests
```python
import pytest
from src.s3_operations.client import S3Operations
from moto import mock_s3

@mock_s3
def test_upload_file():
    """Test file upload to S3"""
    s3_ops = S3Operations()
    
    # Create mock bucket
    s3_ops.client.create_bucket(Bucket='test-bucket')
    
    # Upload file
    with open('/tmp/test.txt', 'w') as f:
        f.write('test content')
    
    result = s3_ops.upload_file('/tmp/test.txt', 'test-bucket', 'test.txt')
    assert result == True
    
    # Verify upload
    response = s3_ops.client.list_objects_v2(Bucket='test-bucket')
    assert len(response['Contents']) == 1
```

---

## Expert Level

### Enterprise Architecture (Steps 76-90)

#### Step 76: Design Multi-Account Strategy
- Implement AWS Organizations structure
- Create separate accounts for dev, staging, prod
- Set up cross-account IAM roles
- **Architecture**: Multi-account design complete

#### Step 77: Implement Service Control Policies (SCPs)
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Action": [
      "s3:DeleteBucket",
      "s3:DeleteBucketPolicy"
    ],
    "Resource": "*",
    "Condition": {
      "StringEquals": {
        "aws:RequestedRegion": ["us-east-1", "us-west-2"]
      }
    }
  }]
}
```

#### Step 78: Implement AWS Config Rules for Compliance
```hcl
resource "aws_config_config_rule" "s3_lifecycle_policy_check" {
  name = "s3-lifecycle-policy-check"
  
  source {
    owner             = "AWS"
    source_identifier = "S3_LIFECYCLE_POLICY_CHECK"
  }
  
  depends_on = [aws_config_configuration_recorder.main]
}
```

#### Step 79: Create EventBridge Rules for Automation
```hcl
resource "aws_cloudwatch_event_rule" "s3_lifecycle_trigger" {
  name        = "s3-lifecycle-trigger"
  description = "Trigger on S3 lifecycle events"
  
  event_pattern = jsonencode({
    source      = ["aws.s3"]
    detail-type = ["Object Lifecycle Transition"]
  })
}
```

#### Step 80: Implement Lambda Functions for Advanced Processing
```python
import json
import boto3

def lambda_handler(event, context):
    """Process S3 lifecycle events"""
    s3 = boto3.client('s3')
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Process the event
        print(f"Processing {key} from {bucket}")
        
        # Add custom logic here
        
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
```

#### Step 81: Set Up AWS CloudTrail for Audit
```hcl
resource "aws_cloudtrail" "s3_audit_trail" {
  name                          = "s3-audit-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail_logs.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  
  event_selector {
    read_write_type           = "All"
    include_management_events = true
    
    data_resource {
      type   = "AWS::S3::Object"
      values = ["${aws_s3_bucket.log_bucket.arn}/"]
    }
  }
}
```

#### Step 82: Implement Cost Allocation Tags
```hcl
resource "aws_s3_bucket" "log_bucket" {
  bucket = var.bucket_name
  
  tags = {
    Environment     = var.environment
    Project         = "LogRetention"
    CostCenter      = var.cost_center
    ComplianceLevel = "High"
    DataClass       = "Logs"
    Owner           = var.owner
  }
}
```

#### Step 83: Create Disaster Recovery Plan
- Implement cross-region replication
- Set up backup procedures
- Document recovery procedures
- Test recovery process
- **Document**: DR plan created

#### Step 84: Implement Infrastructure as Code Pipeline
```yaml
# .github/workflows/terraform.yml
name: Terraform CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        
      - name: Terraform Init
        run: terraform init
        
      - name: Terraform Validate
        run: terraform validate
        
      - name: Terraform Plan
        run: terraform plan
        
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve
```

#### Step 85: Set Up Monitoring Dashboard
```python
import boto3

def create_cloudwatch_dashboard():
    """Create CloudWatch dashboard for S3 metrics"""
    cloudwatch = boto3.client('cloudwatch')
    
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "properties": {
                    "metrics": [
                        ["AWS/S3", "BucketSizeBytes", {"stat": "Average"}],
                        [".", "NumberOfObjects", {"stat": "Average"}]
                    ],
                    "period": 300,
                    "stat": "Average",
                    "region": "us-east-1",
                    "title": "S3 Bucket Metrics"
                }
            }
        ]
    }
    
    cloudwatch.put_dashboard(
        DashboardName='S3-Log-Retention-Dashboard',
        DashboardBody=json.dumps(dashboard_body)
    )
```

#### Step 86: Implement Security Hub Integration
```hcl
resource "aws_securityhub_account" "main" {}

resource "aws_securityhub_standards_subscription" "cis" {
  depends_on    = [aws_securityhub_account.main]
  standards_arn = "arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0"
}
```

#### Step 87: Create Automated Compliance Reporting
```python
class ComplianceReporter:
    def __init__(self, s3_client, config_client):
        self.s3 = s3_client
        self.config = config_client
    
    def generate_report(self) -> Dict:
        """Generate comprehensive compliance report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'buckets': [],
            'compliance_status': 'COMPLIANT'
        }
        
        # Check each bucket
        buckets = self.s3.list_buckets()['Buckets']
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            
            # Check lifecycle policy
            try:
                lifecycle = self.s3.get_bucket_lifecycle_configuration(
                    Bucket=bucket_name
                )
                has_policy = True
            except:
                has_policy = False
            
            # Check encryption
            try:
                encryption = self.s3.get_bucket_encryption(
                    Bucket=bucket_name
                )
                is_encrypted = True
            except:
                is_encrypted = False
            
            bucket_compliance = {
                'name': bucket_name,
                'lifecycle_policy': has_policy,
                'encryption': is_encrypted,
                'compliant': has_policy and is_encrypted
            }
            
            report['buckets'].append(bucket_compliance)
            
            if not bucket_compliance['compliant']:
                report['compliance_status'] = 'NON_COMPLIANT'
        
        return report
```

#### Step 88: Implement GitOps Workflow
- Set up Git repository as source of truth
- Implement automated deployment on merge
- Add PR validation checks
- Configure branch protection rules
- **Workflow**: GitOps implemented

#### Step 89: Create Performance Optimization Strategy
- Implement S3 Transfer Acceleration
- Use multipart uploads for large files
- Optimize request patterns
- Implement caching where appropriate
- **Optimization**: Performance tuning complete

#### Step 90: Implement Multi-Region Deployment
```hcl
# Deploy to multiple regions
module "us_east_1_deployment" {
  source = "../../modules/complete-stack"
  
  providers = {
    aws = aws.us-east-1
  }
  
  environment = var.environment
  region      = "us-east-1"
}

module "eu_west_1_deployment" {
  source = "../../modules/complete-stack"
  
  providers = {
    aws = aws.eu-west-1
  }
  
  environment = var.environment
  region      = "eu-west-1"
}
```

### Advanced Operations (Steps 91-100)

#### Step 91: Implement Blue/Green Deployment Strategy
- Create parallel infrastructure
- Test in blue environment
- Switch traffic to green
- Rollback capability
- **Strategy**: Blue/Green deployment ready

#### Step 92: Set Up Chaos Engineering Tests
```python
import random
import boto3

class ChaosTest:
    def __init__(self):
        self.s3 = boto3.client('s3')
    
    def simulate_failure(self, bucket: str):
        """Simulate random failures for testing"""
        scenarios = [
            self.simulate_network_latency,
            self.simulate_throttling,
            self.simulate_partial_failure
        ]
        
        scenario = random.choice(scenarios)
        scenario(bucket)
```

#### Step 93: Implement Advanced Monitoring with X-Ray
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

@xray_recorder.capture('upload_to_s3')
def upload_with_tracing(bucket: str, key: str, data: bytes):
    """Upload with X-Ray tracing"""
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=key, Body=data)
```

#### Step 94: Create Capacity Planning Tool
```python
class CapacityPlanner:
    def __init__(self, s3_client, cloudwatch_client):
        self.s3 = s3_client
        self.cloudwatch = cloudwatch_client
    
    def analyze_growth_trends(self, bucket: str, days: int = 90):
        """Analyze storage growth trends"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/S3',
            MetricName='BucketSizeBytes',
            Dimensions=[
                {'Name': 'BucketName', 'Value': bucket},
                {'Name': 'StorageType', 'Value': 'StandardStorage'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=86400,
            Statistics=['Average']
        )
        
        # Calculate growth rate
        datapoints = sorted(response['Datapoints'], 
                          key=lambda x: x['Timestamp'])
        
        if len(datapoints) >= 2:
            growth_rate = (datapoints[-1]['Average'] - datapoints[0]['Average']) / days
            return {
                'daily_growth_bytes': growth_rate,
                'projected_30_day': datapoints[-1]['Average'] + (growth_rate * 30)
            }
        
        return None
```

#### Step 95: Implement Automated Remediation
```python
class AutoRemediation:
    def __init__(self, s3_client):
        self.s3 = s3_client
    
    def check_and_fix_encryption(self, bucket: str):
        """Check and enable encryption if missing"""
        try:
            self.s3.get_bucket_encryption(Bucket=bucket)
            return True  # Already encrypted
        except:
            # Enable encryption
            self.s3.put_bucket_encryption(
                Bucket=bucket,
                ServerSideEncryptionConfiguration={
                    'Rules': [{
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    }]
                }
            )
            return True
    
    def check_and_fix_lifecycle(self, bucket: str, retention_days: int = 365):
        """Check and apply lifecycle policy if missing"""
        try:
            policy = self.s3.get_bucket_lifecycle_configuration(Bucket=bucket)
            # Validate policy
            return True
        except:
            # Apply default policy
            self.s3.put_bucket_lifecycle_configuration(
                Bucket=bucket,
                LifecycleConfiguration={
                    'Rules': [{
                        'Id': 'auto-remediation-policy',
                        'Status': 'Enabled',
                        'Expiration': {'Days': retention_days}
                    }]
                }
            )
            return True
```

#### Step 96: Create Advanced Analytics Pipeline
```python
import pandas as pd

class LogAnalytics:
    def __init__(self, athena_client, s3_client):
        self.athena = athena_client
        self.s3 = s3_client
    
    def analyze_access_patterns(self, bucket: str):
        """Analyze S3 access logs with Athena"""
        query = f"""
        SELECT 
            DATE_TRUNC('day', timestamp) as day,
            COUNT(*) as request_count,
            operation,
            AVG(bytessent) as avg_bytes
        FROM s3_access_logs
        WHERE bucket = '{bucket}'
        GROUP BY DATE_TRUNC('day', timestamp), operation
        ORDER BY day DESC
        """
        
        # Execute query
        response = self.athena.start_query_execution(
            QueryString=query,
            ResultConfiguration={
                'OutputLocation': 's3://athena-results/'
            }
        )
        
        return response['QueryExecutionId']
```

#### Step 97: Implement Machine Learning for Anomaly Detection
```python
from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
    
    def train(self, historical_data: np.ndarray):
        """Train anomaly detection model"""
        self.model.fit(historical_data)
    
    def detect_anomalies(self, current_data: np.ndarray):
        """Detect anomalies in current data"""
        predictions = self.model.predict(current_data)
        anomalies = current_data[predictions == -1]
        return anomalies
```

#### Step 98: Create Comprehensive Documentation Portal
- Set up MkDocs or similar
- Generate API documentation
- Create architecture diagrams
- Add runbooks and troubleshooting guides
- **Documentation**: Portal complete

#### Step 99: Implement Continuous Compliance Scanning
```python
class ContinuousCompliance:
    def __init__(self, s3_client, scheduler):
        self.s3 = s3_client
        self.scheduler = scheduler
    
    def schedule_compliance_checks(self):
        """Schedule regular compliance checks"""
        self.scheduler.add_job(
            func=self.run_compliance_scan,
            trigger='interval',
            hours=1,
            id='compliance_scan'
        )
    
    def run_compliance_scan(self):
        """Run comprehensive compliance scan"""
        buckets = self.s3.list_buckets()['Buckets']
        results = []
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            checks = {
                'encryption': self.check_encryption(bucket_name),
                'lifecycle': self.check_lifecycle(bucket_name),
                'versioning': self.check_versioning(bucket_name),
                'logging': self.check_logging(bucket_name),
                'public_access': self.check_public_access(bucket_name)
            }
            
            results.append({
                'bucket': bucket_name,
                'checks': checks,
                'compliant': all(checks.values())
            })
        
        return results
```

#### Step 100: Master Level - Full Integration and Optimization
```python
#!/usr/bin/env python3
"""
Complete S3 Log Retention Automation System
Master-level integration of all components
"""

import asyncio
import logging
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

from src.s3_operations.client import S3Operations, AsyncS3Operations
from src.lifecycle_management.manager import LifecycleManager
from src.compliance.validator import ComplianceValidator
from src.monitoring.metrics import MetricsCollector
from src.reporting.generator import ReportGenerator
from src.remediation.auto import AutoRemediation
from src.analytics.processor import LogAnalytics

@dataclass
class SystemConfig:
    """System configuration"""
    aws_region: str
    retention_days: int
    enable_auto_remediation: bool
    compliance_scan_interval: int
    monitoring_enabled: bool

class S3LogRetentionSystem:
    """Complete S3 Log Retention Automation System"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
        self.logger = self._setup_logging()
        
        # Initialize components
        self.s3_ops = S3Operations(region=config.aws_region)
        self.async_s3 = AsyncS3Operations(region=config.aws_region)
        self.lifecycle_mgr = LifecycleManager(self.s3_ops.client)
        self.compliance = ComplianceValidator(config.retention_days)
        self.metrics = MetricsCollector()
        self.remediation = AutoRemediation(self.s3_ops.client)
        
        self.logger.info("S3 Log Retention System initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Set up system logging"""
        logger = logging.getLogger('s3_retention_system')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    async def run_full_compliance_scan(self) -> Dict:
        """Run comprehensive compliance scan"""
        self.logger.info("Starting full compliance scan")
        
        buckets = self.s3_ops.list_buckets()
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_buckets': len(buckets),
            'compliant_buckets': 0,
            'non_compliant_buckets': 0,
            'details': []
        }
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            
            # Check lifecycle policy
            policy = self.lifecycle_mgr.get_lifecycle_policy(bucket_name)
            is_compliant = self.compliance.validate_lifecycle_policy(policy)
            
            if is_compliant:
                results['compliant_buckets'] += 1
            else:
                results['non_compliant_buckets'] += 1
                
                # Auto-remediate if enabled
                if self.config.enable_auto_remediation:
                    self.logger.info(f"Auto-remediating {bucket_name}")
                    self.remediation.check_and_fix_lifecycle(
                        bucket_name, 
                        self.config.retention_days
                    )
            
            results['details'].append({
                'bucket': bucket_name,
                'compliant': is_compliant
            })
        
        self.logger.info("Compliance scan complete")
        return results
    
    async def optimize_all_buckets(self):
        """Optimize all buckets for cost and compliance"""
        self.logger.info("Starting bucket optimization")
        
        buckets = self.s3_ops.list_buckets()
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            
            # Apply optimal lifecycle policy
            self.lifecycle_mgr.set_lifecycle_policy(
                bucket_name,
                self._generate_optimal_policy()
            )
            
            # Enable encryption
            self.remediation.check_and_fix_encryption(bucket_name)
        
        self.logger.info("Optimization complete")
    
    def _generate_optimal_policy(self) -> List[Dict]:
        """Generate optimal lifecycle policy"""
        return [{
            'Id': 'optimal-retention-policy',
            'Status': 'Enabled',
            'Transitions': [
                {
                    'Days': 30,
                    'StorageClass': 'STANDARD_IA'
                },
                {
                    'Days': 90,
                    'StorageClass': 'GLACIER'
                }
            ],
            'Expiration': {
                'Days': self.config.retention_days
            }
        }]
    
    async def run(self):
        """Run the complete system"""
        self.logger.info("Starting S3 Log Retention System")
        
        # Run compliance scan
        compliance_results = await self.run_full_compliance_scan()
        
        # Optimize buckets
        await self.optimize_all_buckets()
        
        # Generate report
        self.logger.info(f"Compliance Results: {compliance_results}")
        
        self.logger.info("System run complete")

async def main():
    """Main entry point"""
    config = SystemConfig(
        aws_region='us-east-1',
        retention_days=365,
        enable_auto_remediation=True,
        compliance_scan_interval=3600,
        monitoring_enabled=True
    )
    
    system = S3LogRetentionSystem(config)
    await system.run()

if __name__ == '__main__':
    asyncio.run(main())
```

---

## Congratulations! 🎉

You have completed all 100 steps from novice to expert level in S3 Log Retention Automation. You now have:

1. ✅ Complete understanding of AWS S3 and lifecycle policies
2. ✅ Comprehensive Terraform infrastructure as code
3. ✅ Advanced Python automation and tooling
4. ✅ Enterprise-grade security and compliance
5. ✅ Monitoring and observability
6. ✅ Disaster recovery and high availability
7. ✅ Cost optimization strategies
8. ✅ CI/CD and GitOps workflows
9. ✅ Advanced analytics and ML integration
10. ✅ Production-ready system architecture

## Next Steps

- Customize the implementation for your specific use case
- Extend the modules with additional features
- Contribute improvements back to the repository
- Share your knowledge with the community

## Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
