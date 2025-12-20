# Makefile for S3 Log Retention Automation
# Provides convenient commands for common operations

.PHONY: help init install test lint format deploy destroy validate clean

# Default target
help:
	@echo "S3 Log Retention Automation - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make init              - Initialize project (install dependencies)"
	@echo "  make install           - Install Python dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test              - Run all tests"
	@echo "  make lint              - Run linters"
	@echo "  make format            - Format code"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy ENV=<env>  - Deploy infrastructure (ENV=dev|staging|prod)"
	@echo "  make plan ENV=<env>    - Plan infrastructure changes"
	@echo "  make destroy ENV=<env> - Destroy infrastructure"
	@echo "  make validate ENV=<env>- Validate deployment"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean             - Clean temporary files"
	@echo "  make docs              - Generate documentation"
	@echo ""

# Initialize project
init: install
	@echo "Installing Terraform..."
	@which terraform > /dev/null || (echo "Please install Terraform manually" && exit 1)
	@echo "Initializing Terraform..."
	cd terraform && terraform init
	@echo "✓ Project initialized"

# Install Python dependencies
install:
	@echo "Creating Python virtual environment..."
	python3 -m venv venv
	@echo "Installing Python dependencies..."
	. venv/bin/activate && pip install -r python/requirements.txt
	. venv/bin/activate && pip install -r python/requirements-dev.txt
	@echo "✓ Dependencies installed"

# Run tests
test:
	@echo "Running Python tests..."
	. venv/bin/activate && cd python && pytest tests/ -v --cov=lib --cov-report=html
	@echo "Running Terraform validation..."
	cd terraform && terraform init -backend=false && terraform validate
	@echo "✓ All tests passed"

# Run linters
lint:
	@echo "Running Python linters..."
	. venv/bin/activate && cd python && flake8 lib/ scripts/ validators/ reporting/ monitoring/
	. venv/bin/activate && cd python && mypy lib/ --ignore-missing-imports
	@echo "Running Terraform format check..."
	cd terraform && terraform fmt -check -recursive
	@echo "✓ Linting complete"

# Format code
format:
	@echo "Formatting Python code..."
	. venv/bin/activate && cd python && black lib/ scripts/ validators/ reporting/ monitoring/
	@echo "Formatting Terraform code..."
	cd terraform && terraform fmt -recursive
	@echo "✓ Code formatted"

# Deploy infrastructure
deploy:
ifndef ENV
	@echo "ERROR: ENV not specified. Usage: make deploy ENV=dev|staging|prod"
	@exit 1
endif
	@echo "Deploying to $(ENV) environment..."
	./scripts/deploy/deploy.sh $(ENV)

# Plan infrastructure changes
plan:
ifndef ENV
	@echo "ERROR: ENV not specified. Usage: make plan ENV=dev|staging|prod"
	@exit 1
endif
	@echo "Planning $(ENV) environment..."
	./scripts/deploy/deploy.sh $(ENV) --plan-only

# Destroy infrastructure
destroy:
ifndef ENV
	@echo "ERROR: ENV not specified. Usage: make destroy ENV=dev|staging|prod"
	@exit 1
endif
	@echo "Destroying $(ENV) environment..."
	./scripts/deploy/deploy.sh $(ENV) --destroy

# Validate deployment
validate:
ifndef ENV
	@echo "ERROR: ENV not specified. Usage: make validate ENV=dev|staging|prod"
	@exit 1
endif
	@echo "Validating $(ENV) environment..."
	./scripts/validate/validate-deployment.sh $(ENV)

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name .terraform -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.tfstate*" -delete 2>/dev/null || true
	rm -rf venv/ htmlcov/ .coverage
	@echo "✓ Cleaned"

# Generate documentation
docs:
	@echo "Documentation is in docs/manual/"
	@echo "View the comprehensive guide:"
	@echo "  - Steps 1-10: docs/manual/01-10-introduction/README.md"
	@echo "  - Steps 11-20: docs/manual/11-20-aws-setup/README.md"
	@echo "  - Steps 21-100: docs/manual/21-100-comprehensive/README.md"

# Check compliance
compliance:
	@echo "Running compliance checks..."
	. venv/bin/activate && python python/validators/compliance_check.py check-all
	@echo "✓ Compliance check complete"
