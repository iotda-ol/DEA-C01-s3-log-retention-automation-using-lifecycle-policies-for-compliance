# Examples

This directory contains example code demonstrating various use cases.

## Basic Examples

Simple examples for getting started:

- `basic/main.py` - Basic lifecycle policy creation
- `basic/upload_logs.py` - Uploading logs to S3

## Advanced Examples

More complex scenarios:

- `advanced/multi_environment.py` - Managing multiple environments
- `advanced/cost_optimization.py` - Cost analysis and optimization
- `advanced/compliance_reporting.py` - Generating compliance reports

## Multi-Account Examples

Enterprise scenarios:

- `multi-account/cross_account.py` - Cross-account log aggregation
- `multi-account/organization_wide.py` - AWS Organizations integration

## Running Examples

Each example is a standalone Python script:

```bash
cd examples/basic
python main.py
```

Update configuration variables in each script before running.

## Prerequisites

- AWS credentials configured
- S3 buckets created
- Python dependencies installed
- Configuration files updated

## Configuration

Examples use configuration from `configs/config.yaml`. Update this file with your settings.
