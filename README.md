# S3 Log Retention Automation Using Lifecycle Policies for Compliance (DEA-C01)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Terraform](https://img.shields.io/badge/Terraform-1.0+-purple.svg)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20CloudWatch-orange.svg)](https://aws.amazon.com/)

An enterprise-grade solution for automating S3 log retention using lifecycle policies to meet compliance requirements. Features comprehensive documentation (100-step guide from novice to expert), modular Terraform infrastructure, and Python automation tools.

## 🎯 Features

- **Automated Lifecycle Management**: Intelligent storage class transitions and deletions
- **Compliance-Ready**: Pre-configured policies for GDPR, SOC2, HIPAA, PCI-DSS
- **Cost-Optimized**: Automatic tiering to reduce storage costs by up to 95%
- **Modular Architecture**: Reusable Terraform modules and Python packages
- **Comprehensive Monitoring**: CloudWatch dashboards and alarms
- **Security-First**: Encryption, access control, and audit trails
- **Multi-Environment**: Development, staging, and production configurations
- **Extensive Documentation**: 100-step guide from beginner to expert

## 📚 Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [Python](https://www.python.org/downloads/) >= 3.9
- [AWS CLI](https://aws.amazon.com/cli/) configured

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance
```

2. **Install Python dependencies**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Install the package**

```bash
pip install -e .
```

### Deploy Infrastructure

1. **Initialize Terraform**

```bash
cd terraform
terraform init
```

2. **Configure your environment**

Edit `terraform/environments/dev.tfvars` with your settings:

```hcl
log_bucket_name = "your-unique-bucket-name"
aws_region      = "us-east-1"
retention_days  = 365
```

3. **Deploy**

```bash
terraform plan -var-file=environments/dev.tfvars
terraform apply -var-file=environments/dev.tfvars
```

### Use Python CLI

```bash
# List logs
s3-log-retention list-logs --bucket your-bucket-name

# Create lifecycle policy
s3-log-retention create-policy \
  --bucket your-bucket-name \
  --rule-id my-retention-policy \
  --retention-days 365

# Validate policy
s3-log-retention validate-policy --bucket your-bucket-name
```

## 📖 Documentation

### Getting Started

- **[100-Step Guide](docs/STEP_BY_STEP_GUIDE.md)** - Comprehensive guide from novice to expert
- **[Architecture Overview](docs/architecture/overview.md)** - Solution architecture
- **[Repository Structure](docs/architecture/repository_structure.md)** - How the code is organized

### Terraform

- **[Terraform README](terraform/README.md)** - Infrastructure documentation
- **[Module Documentation](terraform/modules/)** - Individual module docs
- **[Environment Configs](terraform/environments/)** - Environment-specific settings

### Python

- **[Source Code README](src/README.md)** - Python package documentation
- **[API Reference](docs/api/)** - Detailed API documentation
- **[Examples](examples/)** - Code examples

### Operations

- **[Deployment Guide](docs/operations/deployment.md)** - How to deploy
- **[Runbooks](docs/runbooks/)** - Operational procedures
- **[Troubleshooting](docs/operations/troubleshooting.md)** - Common issues

## 🏗️ Architecture

```
┌─────────────┐
│ Log Sources │
└──────┬──────┘
       ↓
┌─────────────────────────────────────────┐
│           S3 Log Bucket                 │
│  ┌────────────────────────────────┐    │
│  │   Lifecycle Policies           │    │
│  │  • Transitions                 │    │
│  │  • Expiration                  │    │
│  │  • Compliance Rules            │    │
│  └────────────────────────────────┘    │
└───────────┬─────────────────────────────┘
            ↓
  ┌──────────────────────────┐
  │ Storage Class Transitions│
  ├──────────────────────────┤
  │ Standard (0-30d)         │
  │ Standard-IA (30-90d)     │
  │ Glacier (90-365d)        │
  │ Deep Archive (365d+)     │
  └──────────────────────────┘
            ↓
  ┌──────────────────────────┐
  │  CloudWatch Monitoring   │
  │  • Dashboards            │
  │  • Alarms                │
  │  • Cost Tracking         │
  └──────────────────────────┘
```

## 📂 Repository Structure

```
├── docs/                    # Comprehensive documentation
│   ├── STEP_BY_STEP_GUIDE.md
│   ├── architecture/
│   ├── concepts/
│   └── ...
├── terraform/              # Infrastructure as Code
│   ├── modules/           # Reusable Terraform modules
│   ├── environments/      # Environment configs
│   └── main.tf
├── src/                    # Python source code
│   ├── s3_log_retention/  # Main package
│   ├── cli/               # Command-line interface
│   ├── compliance/        # Compliance tools
│   └── monitoring/        # Monitoring utilities
├── tests/                  # Comprehensive test suite
├── scripts/                # Utility scripts
├── examples/               # Example implementations
└── configs/                # Configuration files
```

## 🔧 Key Components

### Terraform Modules

- **s3-bucket**: Secure S3 bucket with encryption and versioning
- **lifecycle-policy**: Automated retention and transitions
- **iam**: IAM roles and policies for access control
- **cloudwatch**: Monitoring dashboards and alarms
- **sns**: Alerting and notifications

### Python Packages

- **s3_log_retention**: Core S3 operations and lifecycle management
- **cli**: User-friendly command-line interface
- **compliance**: Compliance reporting and validation
- **monitoring**: Anomaly detection and alerting
- **finops**: Cost analysis and optimization

## 💰 Cost Optimization

Lifecycle policies can reduce storage costs significantly:

- **Standard to Standard-IA**: ~46% savings after 30 days
- **Standard-IA to Glacier**: ~82% savings after 90 days
- **Glacier to Deep Archive**: ~96% savings after 180 days

Example savings for 1TB of logs over 1 year:
- Without lifecycle: ~$276/year
- With lifecycle: ~$50/year
- **Savings: $226/year (82%)**

## 🔒 Security

- **Encryption at rest**: AES-256 (SSE-S3) or KMS
- **Encryption in transit**: TLS/SSL for all API calls
- **Access control**: IAM policies and bucket policies
- **Audit trail**: CloudTrail integration
- **Compliance**: GDPR, SOC2, HIPAA, PCI-DSS ready

## 🧪 Testing

Run the test suite:

```bash
pytest
```

With coverage:

```bash
pytest --cov=src --cov-report=html
```

## 🚀 CI/CD

The project includes GitHub Actions workflows for:

- Automated testing
- Terraform validation
- Security scanning
- Documentation generation

## 📊 Monitoring

CloudWatch dashboards provide visibility into:

- Bucket size and object count
- Storage class distribution
- Cost trends
- Access patterns
- Policy compliance

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/community/contributing.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the [docs](docs/) directory
- **Examples**: See [examples](examples/) for code samples
- **Issues**: Report bugs via [GitHub Issues](https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance/issues)

## 🎓 Learning Path

1. **Novice**: Start with [Step-by-Step Guide](docs/STEP_BY_STEP_GUIDE.md) steps 1-20
2. **Beginner**: Complete steps 21-50 for AWS and Terraform basics
3. **Intermediate**: Work through steps 51-80 for implementation
4. **Advanced**: Master steps 81-95 for optimization
5. **Expert**: Achieve steps 96-100 for mastery

## 🏆 Best Practices

This project follows AWS Well-Architected Framework principles:

- **Operational Excellence**: Automated operations, IaC
- **Security**: Encryption, least privilege, audit trails
- **Reliability**: High availability, automatic failover
- **Performance Efficiency**: Right-sized resources
- **Cost Optimization**: Lifecycle policies, monitoring
- **Sustainability**: Efficient resource usage

## 🔗 Related Projects

- [AWS S3 Lifecycle Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

**Made with ❤️ for DEA-C01 Data Engineering on AWS**
# S3 Log Retention Automation with Lifecycle Policies

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Terraform](https://img.shields.io/badge/Terraform-1.0+-purple.svg)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)

An enterprise-grade, automated log retention solution using Amazon S3 Lifecycle policies. This repository demonstrates best practices for implementing compliant, cost-effective log storage following DEA-C01 (AWS Certified Data Engineer - Associate) principles.

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance

# Install Python dependencies
pip install -r python/requirements.txt

# Deploy basic example
cd examples/basic
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your bucket name
terraform init
terraform apply

# Verify deployment
python3 -m python.src.cli.main list-buckets
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Examples](#examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Automated Lifecycle Management
- **Intelligent Tiering**: Automatic transitions between storage classes (Standard → Standard-IA → Glacier)
- **Compliance**: Configurable retention periods (default 365 days)
- **Cost Optimization**: Up to 70% cost reduction through automated tiering
- **Version Management**: Automated cleanup of noncurrent versions

### Security & Compliance
- **Encryption**: AES256 or AWS KMS encryption at rest
- **Access Control**: IAM roles with least privilege
- **Public Access Blocking**: Enforced by default
- **Audit Trail**: CloudTrail and S3 access logging integration

### Infrastructure as Code
- **Modular Terraform**: Reusable, composable modules
- **Multi-Environment**: Support for dev, staging, production
- **State Management**: Remote backend with state locking
- **Validation**: Built-in configuration validation

### Python Utilities
- **CLI Tool**: Comprehensive command-line interface
- **Policy Validation**: Automatic compliance checking
- **Compliance Reporting**: Text and JSON report formats
- **S3 Operations**: High-level Python API for S3

### Monitoring & Observability
- **CloudWatch Dashboards**: Real-time metrics visualization
- **Automated Alarms**: Configurable thresholds and notifications
- **Cost Tracking**: Monitor storage costs and trends
- **Health Checks**: Continuous validation

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Servers   │────▶│  S3 Bucket  │────▶│  Lifecycle  │
│Applications │     │  Encrypted  │     │   Policies  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                     │
                           │                     │
                           ▼                     ▼
                    ┌─────────────┐     ┌─────────────┐
                    │ CloudWatch  │     │  Automatic  │
                    │ Monitoring  │     │  Deletion   │
                    └─────────────┘     └─────────────┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## 📁 Project Structure

```
.
├── terraform/                  # Terraform infrastructure code
│   └── modules/               # Reusable Terraform modules
│       ├── s3_bucket/         # S3 bucket configuration
│       ├── lifecycle_policy/  # Lifecycle policy management
│       ├── iam/               # IAM roles and policies
│       └── monitoring/        # CloudWatch monitoring
│
├── python/                    # Python utilities and tools
│   ├── src/                   # Source code
│   │   ├── s3_ops/           # S3 operations module
│   │   ├── policy_validator/ # Policy validation
│   │   ├── compliance_reporter/ # Compliance reporting
│   │   └── cli/              # Command-line interface
│   └── tests/                # Test suite
│       ├── unit/             # Unit tests
│       └── integration/      # Integration tests
│
├── examples/                  # Example configurations
│   ├── basic/                # Basic deployment example
│   ├── advanced/             # Advanced features
│   └── multi_bucket/         # Multi-bucket setup
│
├── scripts/                   # Automation scripts
│   ├── deploy.sh             # Deployment automation
│   ├── validate.sh           # Validation script
│   └── cleanup.sh            # Resource cleanup
│
└── docs/                      # Documentation
    ├── ARCHITECTURE.md        # Architecture details
    ├── API.md                # API documentation
    └── TROUBLESHOOTING.md    # Troubleshooting guide
```

## 📚 Documentation

- **[100-Step Manual](MANUAL.md)**: Comprehensive guide from novice to expert
- **[Quick Start Guide](QUICKSTART.md)**: Get started in 5 minutes
- **[Architecture Documentation](docs/ARCHITECTURE.md)**: System design and components
- **[Contributing Guidelines](CONTRIBUTING.md)**: How to contribute

## 🔧 Prerequisites

- **AWS Account**: With appropriate permissions
- **AWS CLI**: Version 2.x ([Installation Guide](https://aws.amazon.com/cli/))
- **Terraform**: Version 1.0+ ([Download](https://www.terraform.io/downloads))
- **Python**: Version 3.8+ ([Download](https://www.python.org/downloads/))

## 💻 Usage

### Using Python CLI

```bash
# List all buckets
python3 -m python.src.cli.main list-buckets

# Get bucket information
python3 -m python.src.cli.main bucket-info my-bucket

# Validate lifecycle policy
python3 -m python.src.cli.main validate-policy my-bucket

# Generate compliance report
python3 -m python.src.cli.main compliance-report my-bucket

# Export report to JSON
python3 -m python.src.cli.main compliance-report my-bucket \
  --format json --output report.json
```

### Using Terraform

```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply configuration
terraform apply

# Destroy resources
terraform destroy
```

### Using Automation Scripts

```bash
# Deploy infrastructure
./scripts/deploy.sh basic

# Validate deployment
./scripts/validate.sh my-bucket-name

# Clean up resources
./scripts/cleanup.sh basic
```

## 📖 Examples

### Basic Deployment

Minimal configuration for standard log retention:

```bash
cd examples/basic
terraform apply
```

### Advanced Deployment

With KMS encryption, cross-account access, and custom monitoring:

```bash
cd examples/advanced
terraform apply
```

### Multi-Bucket Deployment

Manage multiple buckets with different policies:

```bash
cd examples/multi_bucket
terraform apply
```

## 🧪 Testing

### Run Unit Tests

```bash
cd python
python3 -m pytest tests/unit/ -v
```

### Run Integration Tests

```bash
python3 -m pytest tests/integration/ -v
```

### Run All Tests with Coverage

```bash
python3 -m pytest tests/ --cov=src --cov-report=html
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- AWS S3 Documentation
- Terraform AWS Provider
- DEA-C01 Certification Guide
- Open Source Community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance/issues)
- **Discussions**: [GitHub Discussions](https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance/discussions)

---

**Built with ❤️ for the AWS Data Engineering Community**
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
- ℹ️ **S3 Access Logging**: Optional (requires separate bucket to avoid recursive logging)

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

*Cost assumptions (US-East-1, December 2024 pricing):
- 1TB new logs per month (12TB total over 12 months)
- STANDARD: $0.023/GB/month
- STANDARD_IA: $0.0125/GB/month (after 90 days)
- GLACIER: $0.004/GB/month (after 180 days)
- Lambda approach includes estimated compute costs ($0.20/1M requests)
- Actual costs vary by region, access patterns, and retrieval frequency

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
   git clone https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
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

- `bucket_name`: **[REQUIRED]** Globally unique S3 bucket name (must be unique across all AWS accounts)
- `retention_days`: Number of days to retain logs (default: 365)
- `transition_to_ia_days`: Days before moving to Infrequent Access (default: 90)
- `transition_to_glacier_days`: Days before moving to Glacier (default: 180)
- `noncurrent_transition_days`: Days before moving noncurrent versions to IA (default: 30)
- `noncurrent_expiration_days`: Days before deleting noncurrent versions (default: 90)
- `multipart_cleanup_days`: Days before aborting incomplete multipart uploads (default: 7)
- `enable_versioning`: Enable/disable object versioning (default: true)
- `kms_key_id`: Optional KMS key for encryption (default: null, uses AES-256)
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

### Enable S3 Access Logging (Optional)

**Note**: S3 access logging to the same bucket creates a recursive logging loop. If you need access logs, create a separate bucket:

```bash
# Create a separate bucket for access logs
aws s3 mb s3://my-access-logs-bucket

# Enable logging via Terraform by uncommenting the aws_s3_bucket_logging resource
# in main.tf and setting target_bucket to your access logs bucket
```

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
- ✅ Noncurrent version cleanup configured
- ✅ Incomplete multipart upload cleanup configured
- ⚠️ Access logging (requires separate bucket to avoid recursive logging)
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
