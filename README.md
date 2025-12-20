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
