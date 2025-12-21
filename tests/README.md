# Tests

This directory contains the test suite for S3 log retention automation.

## Test Structure

```
tests/
├── conftest.py          # Pytest configuration and fixtures
├── unit/                # Unit tests
│   ├── test_s3_utils.py
│   ├── test_lifecycle.py
│   └── test_cost_analysis.py
├── integration/         # Integration tests
│   └── test_end_to_end.py
└── e2e/                # End-to-end tests
    └── test_deployment.py
```

## Running Tests

### Run all tests

```bash
pytest
```

### Run unit tests only

```bash
pytest tests/unit/
```

### Run with coverage

```bash
pytest --cov=src --cov-report=html
```

### Run specific test file

```bash
pytest tests/unit/test_s3_utils.py
```

## Test Requirements

Install test dependencies:

```bash
pip install -r requirements.txt
```

## Mocking

Tests use `moto` library to mock AWS services. No real AWS resources are created during unit tests.

## CI/CD Integration

Tests are automatically run in CI/CD pipeline on every commit.
