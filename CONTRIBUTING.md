# Contributing to S3 Log Retention Automation

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details

### Suggesting Enhancements

1. Check if the enhancement has been suggested
2. Use the feature request template
3. Clearly describe the use case
4. Explain why it would be useful

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code (`black src/`, `terraform fmt -recursive terraform/`)
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

See [Development Environment Setup](docs/setup/environment.md)

## Coding Standards

### Python

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Aim for 80%+ test coverage
- Use Black for formatting
- Use pylint for linting

### Terraform

- Use consistent naming conventions
- Document all variables
- Use modules for reusability
- Run `terraform fmt` before committing
- Validate with `terraform validate`

### Documentation

- Use Markdown for documentation
- Keep language clear and concise
- Include code examples
- Update README when adding features

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_s3_utils.py
```

## Commit Messages

Use clear, descriptive commit messages:

```
Add feature: Implement cost analysis module

- Add CostAnalyzer class
- Implement cost calculation methods
- Add unit tests
- Update documentation
```

Format:
- Use present tense ("Add feature" not "Added feature")
- First line: brief summary (50 chars max)
- Blank line
- Detailed description (if needed)

## Review Process

1. Maintainers review all pull requests
2. At least one approval required
3. All CI checks must pass
4. Address review comments
5. Squash commits before merge

## Release Process

1. Update version in `setup.py` and `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag (`git tag -a v1.0.0 -m "Release v1.0.0"`)
4. Push tag (`git push origin v1.0.0`)
5. GitHub Actions will create release

## Questions?

- Open an issue for questions
- Join discussions
- Check documentation first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
