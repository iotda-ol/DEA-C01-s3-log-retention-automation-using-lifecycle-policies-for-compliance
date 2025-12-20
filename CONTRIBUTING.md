# Contributing to S3 Log Retention Automation

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards

- Be respectful and professional
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

## Getting Started

### Prerequisites

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
   cd DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/iotda-ol/DEA-C01-s3-log-retention-automation-using-lifecycle-policies-for-compliance.git
   ```

4. Install dependencies:
   ```bash
   pip install -r python/requirements.txt
   ```

### Development Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r python/requirements.txt
   ```

3. Configure AWS credentials:
   ```bash
   aws configure
   ```

## Development Workflow

### Creating a Branch

1. Sync with upstream:
   ```bash
   git checkout main
   git pull upstream main
   ```

2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

   Branch naming conventions:
   - `feature/` - New features
   - `fix/` - Bug fixes
   - `docs/` - Documentation changes
   - `refactor/` - Code refactoring
   - `test/` - Test additions or modifications

### Making Changes

1. Make your changes in logical commits
2. Write meaningful commit messages
3. Test your changes thoroughly
4. Update documentation as needed

## Coding Standards

### Terraform

1. **Formatting**:
   ```bash
   terraform fmt -recursive
   ```

2. **Validation**:
   ```bash
   terraform validate
   ```

3. **Best Practices**:
   - Use variables for configurable values
   - Include descriptions for all variables
   - Use data sources to reference existing resources
   - Add comments for complex logic
   - Follow naming conventions: `resource_type_purpose`

4. **Module Guidelines**:
   - One module per logical component
   - Include `variables.tf`, `main.tf`, `outputs.tf`
   - Document module usage in README
   - Version modules appropriately

### Python

1. **Code Style**:
   ```bash
   # Format with Black
   black python/src python/tests

   # Lint with Flake8
   flake8 python/src python/tests

   # Type check with MyPy
   mypy python/src
   ```

2. **Best Practices**:
   - Follow PEP 8 style guide
   - Use type hints
   - Write docstrings for functions and classes
   - Handle exceptions appropriately
   - Use meaningful variable names

3. **Example**:
   ```python
   def calculate_bucket_size(bucket_name: str) -> Dict[str, Any]:
       """
       Calculate total size of objects in S3 bucket.

       Args:
           bucket_name: Name of the S3 bucket

       Returns:
           Dictionary with size metrics

       Raises:
           ClientError: If S3 API call fails
       """
       # Implementation
   ```

### Documentation

1. **Markdown**:
   - Use proper heading hierarchy
   - Include code examples
   - Add links to related documentation
   - Keep lines under 100 characters

2. **Code Comments**:
   - Explain *why*, not *what*
   - Keep comments up to date
   - Use TODO for future improvements

## Testing Guidelines

### Unit Tests

1. **Writing Tests**:
   ```python
   import pytest
   from unittest.mock import Mock, patch

   def test_list_buckets():
       """Test bucket listing functionality"""
       # Arrange
       mock_client = Mock()
       mock_client.list_buckets.return_value = {'Buckets': []}

       # Act
       result = list_buckets(mock_client)

       # Assert
       assert len(result) == 0
   ```

2. **Running Tests**:
   ```bash
   # Run all tests
   pytest python/tests/

   # Run specific test file
   pytest python/tests/unit/test_s3_client.py

   # Run with coverage
   pytest --cov=python/src --cov-report=html
   ```

### Integration Tests

1. Use moto for AWS service mocking
2. Clean up resources after tests
3. Test error conditions
4. Verify end-to-end workflows

### Terraform Tests

1. **Validation**:
   ```bash
   terraform validate
   terraform fmt -check
   ```

2. **Plan Testing**:
   ```bash
   terraform plan -out=tfplan
   ```

## Documentation

### What to Document

1. **Code Changes**:
   - Update relevant documentation
   - Add inline comments for complex logic
   - Update README if adding features

2. **New Features**:
   - Add examples to `examples/` directory
   - Update MANUAL.md if applicable
   - Create tutorial in `docs/`

3. **API Changes**:
   - Update API documentation
   - Add migration guide if breaking changes
   - Version changes appropriately

### Documentation Structure

```markdown
# Feature Name

## Overview
Brief description of the feature

## Usage
Code examples and common use cases

## Configuration
Configuration options and parameters

## Examples
Step-by-step examples

## Troubleshooting
Common issues and solutions
```

## Submitting Changes

### Before Submitting

1. **Self-Review**:
   - [ ] Code follows style guidelines
   - [ ] Tests pass locally
   - [ ] Documentation is updated
   - [ ] No unnecessary files committed
   - [ ] Commit messages are clear

2. **Testing Checklist**:
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Terraform validates
   - [ ] Manual testing completed

### Pull Request Process

1. **Push Changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**:
   - Go to GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out PR template

3. **PR Description**:
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests
   - [ ] Integration tests
   - [ ] Manual testing

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] All tests pass
   ```

4. **Review Process**:
   - Address reviewer feedback
   - Make requested changes
   - Keep PR updated with main branch

### Commit Message Guidelines

Format:
```
type(scope): subject

body

footer
```

Examples:
```
feat(s3): add support for intelligent tiering

Add configuration options for S3 Intelligent-Tiering storage class
in the lifecycle policy module.

Closes #123
```

```
fix(cli): handle missing lifecycle configuration

Fix crash when bucket has no lifecycle policy configured.
Now returns helpful error message instead.

Fixes #456
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Creating a Release

1. Update version numbers
2. Update CHANGELOG.md
3. Create git tag
4. Push changes and tag
5. Create GitHub release

## Questions?

- Open an issue for bugs or feature requests
- Use discussions for questions
- Contact maintainers for security issues

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
