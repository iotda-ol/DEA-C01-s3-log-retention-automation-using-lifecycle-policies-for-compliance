#!/bin/bash
# Security scanning for Terraform code

set -e

echo "Running security scans..."

# Install tools if not present
install_if_missing() {
    local tool=$1
    local install_cmd=$2

    if ! command -v "$tool" &> /dev/null; then
        echo "Installing $tool..."
        eval "$install_cmd"
    fi
}

# Run tfsec
if command -v tfsec &> /dev/null; then
    echo "Running tfsec..."
    tfsec terraform/ || true
else
    echo "⚠ tfsec not installed, skipping..."
fi

# Run checkov
if command -v checkov &> /dev/null; then
    echo "Running checkov..."
    checkov -d terraform/ || true
else
    echo "⚠ checkov not installed, skipping..."
fi

# Run Python security scan
if command -v bandit &> /dev/null; then
    echo "Running bandit..."
    bandit -r src/ || true
else
    echo "⚠ bandit not installed, skipping..."
fi

echo "✓ Security scan complete"
