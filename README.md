# S3 Log Retention Automation

Automated S3 log retention solution using lifecycle policies for compliance. This repository provides a complete, production-ready implementation with:

- 🎓 **100-step instructions** from novice to expert
- 🏗️ **Modular Terraform infrastructure** with reusable components
- 🐍 **Python automation tools** for lifecycle management
- ✅ **Compliance validation** and reporting
- 📊 **Monitoring and observability**
- 🔒 **Security best practices**

## Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- Python 3.8+
- Terraform 1.0+

### Installation

```bash
# Clone the repository
git clone https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Usage

#### Python CLI

```bash
# List all buckets
python python/main.py list-buckets

# Check lifecycle policy
python python/main.py check-policy my-bucket

# Apply lifecycle policy
python python/main.py apply-policy my-bucket --retention-days 365

# Validate compliance
python python/main.py validate my-bucket

# Scan all buckets
python python/main.py scan-all
```

#### Terraform Deployment

```bash
cd terraform/environments/dev

# Review configuration
cat terraform.tfvars

# Plan deployment
terraform plan

# Apply infrastructure
terraform apply
```

## Project Structure

```
.
├── docs/                           # Documentation
│   ├── INSTRUCTIONS.md            # 100-step guide
│   ├── beginner/                  # Beginner tutorials
│   ├── intermediate/              # Intermediate guides
│   ├── advanced/                  # Advanced topics
│   └── expert/                    # Expert-level content
│
├── terraform/                     # Infrastructure as Code
│   ├── modules/                   # Reusable Terraform modules
│   │   ├── s3-bucket/            # S3 bucket module
│   │   ├── lifecycle-policy/     # Lifecycle policy module
│   │   └── iam/                  # IAM roles and policies
│   └── environments/              # Environment configurations
│       ├── dev/                   # Development
│       ├── staging/               # Staging
│       └── prod/                  # Production
│
├── python/                        # Python automation
│   ├── src/                       # Source code
│   │   ├── s3_operations/        # S3 operations module
│   │   ├── lifecycle_management/ # Lifecycle management
│   │   ├── compliance/           # Compliance validation
│   │   ├── monitoring/           # Monitoring utilities
│   │   └── utils/                # Utility functions
│   ├── tests/                     # Test suite
│   ├── main.py                    # CLI entry point
│   └── requirements.txt           # Dependencies
│
├── config/                        # Configuration files
│   ├── dev/                       # Development config
│   ├── staging/                   # Staging config
│   └── prod/                      # Production config
│
├── examples/                      # Usage examples
│   ├── basic/                     # Basic examples
│   ├── advanced/                  # Advanced examples
│   └── enterprise/                # Enterprise patterns
│
└── scripts/                       # Helper scripts
    └── setup.sh                   # Quick setup script
```

## Features

### Terraform Modules

- **S3 Bucket Module**: Secure bucket creation with encryption, versioning, and logging
- **Lifecycle Policy Module**: Flexible lifecycle rules with transitions and expirations
- **IAM Module**: Least-privilege access roles and policies

### Python Tools

- **S3 Operations**: Comprehensive S3 client wrapper
- **Lifecycle Management**: Create, apply, and manage lifecycle policies
- **Compliance Validation**: Automated compliance checking
- **CLI Interface**: User-friendly command-line tool

### Documentation

- **100-Step Guide**: Complete learning path from beginner to expert
- **API Documentation**: Detailed module and function documentation
- **Architecture Guides**: System design and best practices
- **Tutorials**: Step-by-step implementation guides

## Compliance

This solution helps meet compliance requirements by:

- Automatically deleting logs after 365 days (configurable)
- Encrypting data at rest
- Enabling versioning for audit trails
- Blocking public access
- Providing compliance validation and reporting

## Development

### Running Tests

```bash
cd python
pytest tests/ -v
```

### Code Style

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### Terraform Validation

```bash
cd terraform
terraform fmt -recursive
terraform validate
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
- Open an issue on GitHub
- Check the documentation in `docs/`
- Review the 100-step guide in `docs/INSTRUCTIONS.md`

## Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
