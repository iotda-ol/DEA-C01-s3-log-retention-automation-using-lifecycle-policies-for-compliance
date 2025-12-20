# Repository Structure

This document describes the organization of the S3 Log Retention Automation repository.

## Directory Tree

```
DEA-C01-s3-log-retention-automation/
├── docs/                          # Documentation
│   ├── STEP_BY_STEP_GUIDE.md     # 100-step manual (novice to expert)
│   ├── architecture/              # Architecture documentation
│   ├── concepts/                  # Conceptual documentation
│   ├── setup/                     # Setup guides
│   ├── terraform/                 # Terraform documentation
│   ├── python/                    # Python documentation
│   ├── aws/                       # AWS service documentation
│   ├── security/                  # Security best practices
│   ├── compliance/                # Compliance requirements
│   ├── cost/                      # Cost optimization
│   ├── cicd/                      # CI/CD documentation
│   ├── testing/                   # Testing guides
│   ├── operations/                # Operational runbooks
│   ├── optimization/              # Performance optimization
│   ├── advanced/                  # Advanced topics
│   ├── runbooks/                  # Operational runbooks
│   ├── api/                       # API reference
│   └── community/                 # Community guidelines
│
├── terraform/                     # Infrastructure as Code
│   ├── main.tf                    # Root module configuration
│   ├── variables.tf               # Input variables
│   ├── outputs.tf                 # Output values
│   ├── providers.tf               # Provider configuration
│   ├── backend.tf                 # State backend (create this)
│   ├── modules/                   # Reusable Terraform modules
│   │   ├── s3-bucket/            # S3 bucket module
│   │   ├── lifecycle-policy/      # Lifecycle policy module
│   │   ├── iam/                   # IAM roles and policies
│   │   ├── cloudwatch/            # Monitoring module
│   │   ├── sns/                   # Alerting module
│   │   └── s3-replication/        # Cross-region replication
│   └── environments/              # Environment-specific configs
│       ├── dev.tfvars
│       ├── staging.tfvars
│       └── prod.tfvars
│
├── src/                           # Python source code
│   ├── s3_log_retention/         # Main package
│   │   ├── __init__.py
│   │   ├── s3_utils.py           # S3 utilities
│   │   ├── lifecycle.py          # Lifecycle management
│   │   ├── logger.py             # Logging configuration
│   │   ├── cost_analysis.py      # Cost analysis
│   │   └── validator.py          # Validation utilities
│   ├── cli/                       # Command-line interface
│   │   ├── __init__.py
│   │   └── main.py
│   ├── compliance/                # Compliance tools
│   │   ├── __init__.py
│   │   └── report_generator.py
│   ├── monitoring/                # Monitoring tools
│   │   ├── __init__.py
│   │   └── anomaly_detection.py
│   └── finops/                    # FinOps tools
│       ├── __init__.py
│       └── optimizer.py
│
├── tests/                         # Test suite
│   ├── conftest.py               # Pytest configuration
│   ├── unit/                      # Unit tests
│   │   ├── test_s3_utils.py
│   │   └── test_lifecycle.py
│   ├── integration/               # Integration tests
│   │   └── test_end_to_end.py
│   └── e2e/                       # End-to-end tests
│       └── test_deployment.py
│
├── scripts/                       # Utility scripts
│   ├── validate_infrastructure.py # Infrastructure validation
│   ├── test_lifecycle.py         # Lifecycle testing
│   ├── generate_docs.sh          # Documentation generation
│   └── security_scan.sh          # Security scanning
│
├── configs/                       # Configuration files
│   ├── config.yaml               # Main configuration
│   ├── config.dev.yaml           # Dev overrides
│   └── config.prod.yaml          # Prod overrides
│
├── examples/                      # Example code
│   ├── basic/                     # Basic examples
│   │   ├── main.py
│   │   └── README.md
│   ├── advanced/                  # Advanced examples
│   │   ├── multi_environment.py
│   │   └── cost_optimization.py
│   └── multi-account/            # Multi-account examples
│       └── cross_account.py
│
├── .github/                       # GitHub configuration
│   └── workflows/                 # GitHub Actions workflows
│       └── main.yml
│
├── .gitignore                     # Git ignore rules
├── README.md                      # Project README
├── requirements.txt               # Python dependencies
├── setup.py                       # Python package setup
└── LICENSE                        # License file
```

## Design Principles

### 1. Modular Organization

- **Terraform modules**: Reusable, composable infrastructure components
- **Python packages**: Well-organized, importable code
- **Clear separation**: Infrastructure, code, tests, docs

### 2. Maximum Reusability

- **DRY principle**: Don't Repeat Yourself
- **Shared modules**: Common patterns extracted
- **Configuration-driven**: Behavior controlled by configs

### 3. Organized Structure

- **Many folders**: Logical grouping of related files
- **Few loose files**: Everything has a place
- **Clear hierarchy**: Easy navigation

### 4. Technology Focus

- **Terraform primary**: Infrastructure as Code
- **Python secondary**: Automation and tooling
- **Minimal other**: Only when necessary

## File Naming Conventions

### Terraform

- `main.tf` - Primary resource definitions
- `variables.tf` - Input variable declarations
- `outputs.tf` - Output value declarations
- `providers.tf` - Provider configuration
- `backend.tf` - State backend configuration

### Python

- `snake_case.py` - Module names
- `ClassName` - Class names
- `function_name()` - Function names
- `CONSTANT_NAME` - Constants

### Documentation

- `UPPERCASE.md` - Important root documents
- `lowercase.md` - Regular documents
- Clear, descriptive names

## Navigation Tips

1. **Start with**: `README.md` for overview
2. **Learn with**: `docs/STEP_BY_STEP_GUIDE.md` for comprehensive guide
3. **Deploy with**: `terraform/` for infrastructure
4. **Automate with**: `src/` for Python tools
5. **Validate with**: `tests/` for testing
6. **Example from**: `examples/` for use cases

## Growth and Scalability

This structure supports:

- Adding new modules
- Extending functionality
- Multiple environments
- Team collaboration
- CI/CD integration
- Documentation expansion
