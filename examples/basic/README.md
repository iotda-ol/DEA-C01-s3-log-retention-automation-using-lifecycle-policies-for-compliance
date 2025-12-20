# Basic Example

This example demonstrates basic usage of the S3 log retention automation.

## What it does

1. Creates a lifecycle policy for log retention
2. Lists existing logs in the bucket
3. Validates the policy configuration

## Prerequisites

- AWS credentials configured
- S3 bucket created
- Python dependencies installed

## Running

```bash
# Update BUCKET_NAME in main.py
python examples/basic/main.py
```

## Expected Output

```
Creating retention policy...
✓ Retention policy created successfully

Listing logs...
Found 0 log files

Validating policy...
Policy is valid
```
