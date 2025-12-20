# DEA-C01: S3 Log Retention Automation Using Lifecycle Policies

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Terraform](https://img.shields.io/badge/Terraform-1.6+-purple.svg)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20CloudWatch-orange.svg)](https://aws.amazon.com/)

Comprehensive, production-ready solution for automated S3 log retention that meets DEA-C01 compliance requirements. This repository provides **modular Terraform infrastructure**, **reusable Python automation libraries**, and a **100-step implementation manual** (from novice to expert).

## 🎯 Key Features

- ✅ **DEA-C01 Compliant**: Automatic 365-day retention with deletion
- ✅ **Cost Optimized**: Up to 96% storage cost reduction through lifecycle transitions
- ✅ **Fully Automated**: Set it and forget it - no manual intervention
- ✅ **Modular Design**: Reusable Terraform modules and Python libraries
- ✅ **Production Ready**: Security best practices, monitoring, and alerting
- ✅ **Well Documented**: 100-step manual from beginner to expert level

## 📊 Cost Savings Example

For **100 GB** of logs stored for 1 year:

| Approach | Monthly Cost | Annual Cost | Savings |
|----------|--------------|-------------|---------|
| All STANDARD (no lifecycle) | $23.00 | $276.00 | Baseline |
| **With Lifecycle Policy** | $0.55 | $6.59 | **98%** ⬇️ |

## 🏗️ Architecture

```
┌─────────────┐
│ Applications│
└──────┬──────┘
       │ Logs
       ▼
┌──────────────────────────────────────┐
│         S3 Bucket (Encrypted)        │
│  ┌────────────────────────────────┐  │
│  │   Lifecycle Policy (DEA-C01)   │  │
│  │  Day 0-30:   STANDARD          │  │
│  │  Day 30-90:  STANDARD_IA       │  │
│  │  Day 90-180: GLACIER           │  │
│  │  Day 180-365: DEEP_ARCHIVE     │  │
│  │  Day 365+:   DELETED           │  │
│  └────────────────────────────────┘  │
└─────────────┬────────────────────────┘
              │
       ┌──────┴──────┐
       ▼             ▼
┌─────────────┐ ┌──────────┐
│ CloudWatch  │ │CloudTrail│
│  Monitoring │ │  Audit   │
└─────────────┘ └──────────┘
```

## 🚀 Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- Terraform 1.6+
- Python 3.8+
- AWS CLI configured

### 1. Clone Repository

```bash
git clone https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance
```

### 2. Initialize Project

```bash
make init
```

### 3. Deploy Infrastructure

```bash
# Deploy to development environment
make deploy ENV=dev

# Deploy to production
make deploy ENV=prod
```

### 4. Verify Deployment

```bash
make validate ENV=dev
```

## 📚 Documentation

### Comprehensive 100-Step Manual

Start from complete novice and progress to expert level:

1. **[Steps 1-10: Introduction & Prerequisites](docs/manual/01-10-introduction/README.md)**
   - Understanding DEA-C01 requirements
   - S3 and lifecycle policy fundamentals
   - Tool installation and setup
   - Cost optimization principles

2. **[Steps 11-20: AWS Account Setup](docs/manual/11-20-aws-setup/README.md)**
   - Billing alerts and cost monitoring
   - IAM security best practices
   - CloudTrail and AWS Config
   - Multi-account strategies

3. **[Steps 21-100: Comprehensive Implementation](docs/manual/21-100-comprehensive/README.md)**
   - S3 bucket design and configuration
   - Lifecycle policy implementation
   - Terraform and Python automation
   - Advanced topics and expert strategies

### Additional Documentation

- **[Architecture](ARCHITECTURE.md)**: System design and component overview
- **[Contributing](CONTRIBUTING.md)**: Guidelines for contributors
- **[Examples](examples/)**: Reference implementations

## 🗂️ Project Structure

```
├── terraform/                 # Infrastructure as Code
│   ├── modules/              # Reusable Terraform modules
│   │   ├── s3-bucket/       # S3 bucket with security
│   │   ├── lifecycle-policy/# Lifecycle management
│   │   ├── iam/             # IAM roles and policies
│   │   └── logging/         # CloudWatch & CloudTrail
│   ├── environments/        # Environment configs (dev/staging/prod)
│   └── main.tf              # Root configuration
│
├── python/                   # Python automation
│   ├── lib/                 # Reusable libraries
│   │   ├── aws_client.py   # AWS client management
│   │   ├── s3_operations.py# S3 operations
│   │   ├── lifecycle_policy.py # Policy templates
│   │   └── config_manager.py   # Configuration
│   ├── scripts/             # CLI tools
│   ├── validators/          # Compliance checking
│   ├── reporting/           # Report generation
│   └── monitoring/          # Metrics and alerting
│
├── docs/                    # Documentation
│   └── manual/             # 100-step implementation guide
│
├── examples/               # Example implementations
│   ├── basic/             # Basic setup
│   ├── advanced/          # Multi-region, advanced features
│   └── compliance/        # Enhanced compliance
│
├── templates/             # Configuration templates
├── scripts/              # Utility scripts
│   ├── deploy/          # Deployment automation
│   ├── validate/        # Validation scripts
│   └── cleanup/         # Cleanup utilities
│
├── tests/               # Automated tests
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── terraform/      # Terraform tests
│
└── Makefile            # Common operations
```

## 🔧 Usage Examples

### Deploy Basic Infrastructure

```bash
cd terraform
terraform init
terraform plan -var-file=environments/dev/terraform.tfvars
terraform apply
```

### Manage Logs with Python CLI

```bash
# Activate virtual environment
source venv/bin/activate

# Create bucket with lifecycle policy
python python/scripts/manage_logs.py create-bucket my-log-bucket-dev
python python/scripts/manage_logs.py apply-lifecycle my-log-bucket-dev --template dea-c01

# Show current lifecycle policy
python python/scripts/manage_logs.py show-lifecycle my-log-bucket-dev

# List objects
python python/scripts/manage_logs.py list-objects my-log-bucket-dev --prefix logs/

# Calculate bucket size
python python/scripts/manage_logs.py bucket-size my-log-bucket-dev
```

### Run Compliance Checks

```bash
# Check single bucket
python python/validators/compliance_check.py check my-log-bucket

# Check all buckets
python python/validators/compliance_check.py check-all
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run linters
make lint

# Format code
make format
```

## 📈 Monitoring

The solution includes comprehensive monitoring:

- **CloudWatch Metrics**: Storage size, object count, request rates
- **CloudWatch Alarms**: Quota exceeded, lifecycle failures
- **CloudTrail**: API audit logging
- **SNS Notifications**: Email/Slack alerts

## 🔒 Security Features

- ✅ Server-side encryption (AES256 or KMS)
- ✅ Versioning enabled
- ✅ Public access blocked
- ✅ IAM least privilege access
- ✅ Audit logging with CloudTrail
- ✅ VPC endpoints support
- ✅ Bucket policies and access points

## 🌍 Multi-Region Support

Deploy across multiple regions for disaster recovery:

```hcl
module "primary_region" {
  source = "./terraform"
  region = "us-east-1"
}

module "dr_region" {
  source = "./terraform"
  region = "us-west-2"
}
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- AWS DEA-C01 certification program
- Terraform and Python communities
- Contributors and maintainers

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance/issues)
- **Documentation**: See `docs/manual/` for comprehensive guides
- **Examples**: Check `examples/` directory

---

**Built with ❤️ for DEA-C01 compliance and cost optimization**
