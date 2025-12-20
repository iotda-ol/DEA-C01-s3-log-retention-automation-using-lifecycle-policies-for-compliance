#!/bin/bash
# Generate Terraform documentation using terraform-docs

set -e

echo "Generating Terraform documentation..."

# Check if terraform-docs is installed
if ! command -v terraform-docs &> /dev/null; then
    echo "terraform-docs not found. Installing..."
    go install github.com/terraform-docs/terraform-docs@latest
fi

# Generate documentation for each module
for module in terraform/modules/*/; do
    echo "Generating docs for $(basename $module)..."
    terraform-docs markdown table "$module" > "$module/README.md"
done

# Generate root module documentation
echo "Generating docs for root module..."
terraform-docs markdown table terraform/ > terraform/TERRAFORM.md

echo "✓ Documentation generated successfully"
