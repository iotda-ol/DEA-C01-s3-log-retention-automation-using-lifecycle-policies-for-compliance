# Contributing Guidelines

Thank you for your interest in contributing to the S3 Log Retention Automation project!

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/DEA-C01-s3-log-retention-automation.git
   cd DEA-C01-s3-log-retention-automation
   ```
3. **Set up development environment**:
   ```bash
   make init
   ```

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

### 2. Make Changes
- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits atomic and focused

### 3. Test Your Changes
```bash
# Run all tests
make test

# Run linters
make lint

# Format code
make format
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: Add new feature"
# or
git commit -m "fix: Fix bug in lifecycle policy"
```

**Commit Message Format**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Build process or auxiliary tool changes

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Coding Standards

### Python

**Style Guide**: PEP 8
```python
# Good
def calculate_storage_cost(size_gb: int, storage_class: str) -> float:
    """
    Calculate storage cost for given size and class.
    
    Args:
        size_gb: Storage size in gigabytes
        storage_class: AWS storage class
        
    Returns:
        Monthly cost in USD
    """
    rates = {
        'STANDARD': 0.023,
        'STANDARD_IA': 0.0125,
        'GLACIER': 0.004
    }
    return size_gb * rates.get(storage_class, 0.023)

# Bad
def calc(s,c):
    return s*0.023
```

**Type Hints**: Always use type hints
```python
from typing import List, Dict, Optional

def process_logs(
    bucket_name: str,
    prefixes: List[str],
    filters: Optional[Dict[str, str]] = None
) -> int:
    pass
```

**Docstrings**: Google style
```python
def function(arg1: str, arg2: int) -> bool:
    """
    Short description.
    
    Longer description with more details about what the
    function does and any important notes.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: If arg2 is negative
        
    Example:
        >>> function("test", 42)
        True
    """
    pass
```

### Terraform

**Style Guide**: HashiCorp Configuration Language
```hcl
# Good
resource "aws_s3_bucket" "logs" {
  bucket = var.bucket_name
  
  tags = merge(
    var.common_tags,
    {
      Name = var.bucket_name
      Purpose = "Log Storage"
    }
  )
}

# Bad
resource "aws_s3_bucket" "logs" {
bucket=var.bucket_name
tags={Name=var.bucket_name}}
```

**Variables**: Always include descriptions
```hcl
variable "retention_days" {
  description = "Number of days to retain logs (DEA-C01 requires max 365)"
  type        = number
  default     = 365
  
  validation {
    condition     = var.retention_days > 0 && var.retention_days <= 365
    error_message = "Retention days must be between 1 and 365."
  }
}
```

## Testing Requirements

### Python Tests
```python
# tests/unit/test_lifecycle_policy.py
import pytest
from lib.lifecycle_policy import LifecyclePolicyManager

def test_dea_c01_compliant_rule():
    """Test DEA-C01 compliant rule creation"""
    rule = LifecyclePolicyManager.create_dea_c01_compliant_rule()
    
    assert rule['ID'] == 'dea-c01-compliance'
    assert rule['Status'] == 'Enabled'
    assert rule['Expiration']['Days'] == 365
    assert len(rule['Transitions']) == 3
```

### Terraform Tests
```bash
# Run terraform validate
cd terraform
terraform init -backend=false
terraform validate

# Run terraform plan
terraform plan -var-file=environments/dev/terraform.tfvars
```

## Documentation

### Code Documentation
- All public functions must have docstrings
- Complex logic should have inline comments
- Update README.md if adding new features

### Manual Updates
If your change affects user workflows:
1. Update relevant section in `docs/manual/`
2. Keep step numbers consistent
3. Add examples where helpful

## Pull Request Process

1. **Update CHANGELOG.md** with your changes
2. **Ensure all tests pass** (`make test`)
3. **Update documentation** if needed
4. **Request review** from maintainers
5. **Address feedback** promptly
6. **Squash commits** if requested

### PR Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows style guide
- [ ] Commits are descriptive
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts

## Review Process

### What Reviewers Look For
- Code quality and clarity
- Test coverage
- Documentation completeness
- Security considerations
- Performance implications
- Backwards compatibility

### Timeline
- Initial review: Within 3 business days
- Follow-up reviews: Within 2 business days
- Merge: After approval from 2 maintainers

## Reporting Issues

### Bug Reports
Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

### Feature Requests
Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Potential impact

## Questions?

- Open a GitHub Discussion
- Check existing documentation
- Review closed issues/PRs

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing! 🎉
