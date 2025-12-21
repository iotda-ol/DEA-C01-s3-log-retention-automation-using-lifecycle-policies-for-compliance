# Python Package

S3 Log Retention Automation - Python utilities and CLI tool.

## Installation

### From Source

```bash
cd python
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

### With Async Support

```bash
pip install -e ".[async]"
```

## Usage

### As a Library

```python
from s3_ops import S3Client
from policy_validator import PolicyValidator
from compliance_reporter import ComplianceReporter

# Initialize clients
s3_client = S3Client(region_name='us-east-1')
policy_validator = PolicyValidator(min_retention_days=365)
compliance_reporter = ComplianceReporter(s3_client, policy_validator)

# List buckets
buckets = s3_client.list_buckets()

# Validate policy
lifecycle_config = s3_client.get_lifecycle_configuration('my-bucket')
validation_result = policy_validator.validate_lifecycle_policy(lifecycle_config)

# Generate compliance report
report = compliance_reporter.generate_bucket_report('my-bucket')
print(compliance_reporter.format_report_text(report))
```

### As a CLI Tool

```bash
# List buckets
python -m python.src.cli.main list-buckets

# Get bucket info
python -m python.src.cli.main bucket-info my-bucket

# Validate policy
python -m python.src.cli.main validate-policy my-bucket

# Generate compliance report
python -m python.src.cli.main compliance-report my-bucket

# Get help
python -m python.src.cli.main --help
```

## Modules

### s3_ops

High-level S3 client with retry logic and error handling.

**Features**:
- List buckets and objects
- Get lifecycle configurations
- Calculate bucket sizes
- Upload/download files
- Manage tags

### policy_validator

Validate lifecycle policies against compliance requirements.

**Features**:
- Policy validation
- Compliance checking
- Security best practices
- Storage class validation

### compliance_reporter

Generate compliance reports in multiple formats.

**Features**:
- Single and multi-bucket reports
- Text and JSON output
- Expiring objects tracking
- Statistics collection

### cli

Command-line interface for easy management.

**Commands**:
- `list-buckets`: List all S3 buckets
- `bucket-info`: Get bucket details
- `validate-policy`: Check policy compliance
- `compliance-report`: Generate reports
- `expiring-objects`: Find objects nearing expiration

## Testing

```bash
# Run unit tests
pytest tests/unit/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_s3_client.py::test_list_buckets
```

## Development

### Code Style

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Adding Tests

Place tests in `tests/unit/` or `tests/integration/` following the naming convention `test_*.py`.

## Documentation

See the main project documentation for detailed usage examples and guides.
