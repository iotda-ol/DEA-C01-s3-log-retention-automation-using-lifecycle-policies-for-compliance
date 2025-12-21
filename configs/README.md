# Configuration Files

This directory contains configuration files for S3 log retention automation.

## Files

- `config.yaml` - Main configuration file
- `config.dev.yaml` - Development environment overrides
- `config.prod.yaml` - Production environment overrides

## Usage

The configuration can be loaded by Python scripts:

```python
import yaml

with open('configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
```

## Configuration Structure

### AWS Section

Configure AWS credentials and region settings.

### Logging Section

Control application logging behavior.

### Retention Section

Define retention policies for different log types.

### Monitoring Section

Configure CloudWatch monitoring and alarms.

### Compliance Section

Specify compliance frameworks and audit requirements.
