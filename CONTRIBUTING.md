# Contributing to S3 Log Retention Automation

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professionalism

## How to Contribute

### Reporting Issues

1. Check existing issues first
2. Use the issue template
3. Provide detailed information:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow coding standards
   - Add tests
   - Update documentation

4. **Test your changes**
   ```bash
   # Python tests
   cd python
   pytest tests/ -v
   
   # Terraform validation
   cd terraform
   terraform fmt -recursive
   terraform validate
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "feat: add new lifecycle policy option"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    pass
```

### Terraform

- Use consistent naming conventions
- Document variables and outputs
- Use modules for reusability
- Format with `terraform fmt`

```hcl
variable "example_var" {
  description = "Clear description"
  type        = string
  default     = "default_value"
  
  validation {
    condition     = length(var.example_var) > 0
    error_message = "Must not be empty."
  }
}
```

## Testing

### Python Tests

- Write tests for new features
- Maintain or improve code coverage
- Use moto for AWS mocking

### Terraform Tests

- Validate all configurations
- Test in isolated environment
- Document manual testing steps

## Documentation

- Update README.md for user-facing changes
- Add inline comments for complex logic
- Update architecture docs for design changes
- Include examples for new features

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG (if applicable)
5. Request review from maintainers

## Release Process

1. Version bump (semver)
2. Update CHANGELOG
3. Tag release
4. Deploy to environments

## Questions?

Open an issue or reach out to maintainers.
