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
