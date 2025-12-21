.PHONY: help install test lint format clean deploy destroy

help:
@echo "Available targets:"
@echo "  install    - Install Python dependencies"
@echo "  test       - Run all tests"
@echo "  lint       - Run linting checks"
@echo "  format     - Format code"
@echo "  clean      - Clean build artifacts"
@echo "  deploy     - Deploy infrastructure"
@echo "  destroy    - Destroy infrastructure"

install:
pip install -r requirements.txt
pip install -e .

test:
pytest tests/ -v --cov=src --cov-report=html

lint:
pylint src/
black --check src/
mypy src/
isort --check-only src/

format:
black src/
isort src/

clean:
rm -rf build/
rm -rf dist/
rm -rf *.egg-info
rm -rf .pytest_cache
rm -rf .coverage
rm -rf htmlcov/
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

deploy:
cd terraform && \
terraform init && \
terraform plan -var-file=environments/dev.tfvars && \
terraform apply -var-file=environments/dev.tfvars

destroy:
cd terraform && \
terraform destroy -var-file=environments/dev.tfvars

.DEFAULT_GOAL := help
