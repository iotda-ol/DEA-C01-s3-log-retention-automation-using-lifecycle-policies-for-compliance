# Source Code

This directory contains the Python source code for S3 log retention automation.

## Package Structure

### s3_log_retention

Main package for S3 log management:

- `s3_utils.py` - S3 operations (upload, list, delete, tag)
- `lifecycle.py` - Lifecycle policy management
- `logger.py` - Structured logging configuration
- `cost_analysis.py` - Cost estimation and optimization
- `validator.py` - Data validation utilities

### cli

Command-line interface:

- `main.py` - CLI entry point with commands

### compliance

Compliance and reporting:

- `report_generator.py` - Generate compliance reports

### monitoring

Monitoring and alerting:

- `anomaly_detection.py` - ML-based anomaly detection

### finops

Financial operations:

- `optimizer.py` - Cost optimization recommendations

## Installation

```bash
pip install -e .
```

## Usage

```python
from s3_log_retention import S3LogManager, LifecyclePolicyManager

# Create managers
s3 = S3LogManager('my-bucket')
lifecycle = LifecyclePolicyManager('my-bucket')

# Create policy
lifecycle.create_retention_policy(
    rule_id='my-rule',
    expiration_days=365
)
```

## CLI Usage

```bash
s3-log-retention list-logs --bucket my-bucket
s3-log-retention create-policy --bucket my-bucket --retention-days 365
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Format code:

```bash
black src/
isort src/
```

Lint code:

```bash
pylint src/
mypy src/
```
