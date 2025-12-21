# Terraform Best Practices

## Code Organization

### Module Structure

```
module/
├── main.tf       # Primary resources
├── variables.tf  # Input variables
├── outputs.tf    # Output values
├── versions.tf   # Version constraints
├── README.md     # Documentation
└── examples/     # Usage examples
```

### Naming Conventions

- **Resources**: `resource_type_purpose`
  ```hcl
  resource "aws_s3_bucket" "log_storage" { }
  ```

- **Variables**: `snake_case`
  ```hcl
  variable "retention_days" { }
  ```

- **Outputs**: descriptive names
  ```hcl
  output "bucket_arn" { }
  ```

## State Management

### Remote State

Always use remote state for team projects:

```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "project/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### State Locking

Prevent concurrent modifications:

```bash
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

## Variables and Outputs

### Variable Validation

```hcl
variable "retention_days" {
  type        = number
  description = "Log retention period in days"
  
  validation {
    condition     = var.retention_days >= 30 && var.retention_days <= 3650
    error_message = "Retention must be between 30 and 3650 days."
  }
}
```

### Sensitive Outputs

```hcl
output "database_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}
```

## Resource Management

### Dependencies

Use `depends_on` explicitly when needed:

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  
  depends_on = [aws_s3_bucket_versioning.logs]
}
```

### Lifecycle Meta-Arguments

```hcl
resource "aws_s3_bucket" "critical" {
  bucket = "critical-data"

  lifecycle {
    prevent_destroy = true
    create_before_destroy = true
  }
}
```

## Security

### Sensitive Data

Never commit sensitive values:

```hcl
# Bad
variable "api_key" {
  default = "secret-key-123"
}

# Good
variable "api_key" {
  type      = string
  sensitive = true
}
```

Use environment variables:
```bash
export TF_VAR_api_key="secret-key-123"
```

## Testing

### Format Check

```bash
terraform fmt -check -recursive
```

### Validation

```bash
terraform validate
```

### Plan Review

```bash
terraform plan -out=tfplan
terraform show tfplan
```

## Documentation

### Variable Documentation

```hcl
variable "bucket_name" {
  description = "Name of the S3 bucket for log storage"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", var.bucket_name))
    error_message = "Bucket name must be lowercase alphanumeric with hyphens."
  }
}
```

### Module Documentation

Use terraform-docs:

```bash
terraform-docs markdown table . > README.md
```

## Performance

### Parallel Operations

Terraform automatically parallelizes, but you can control:

```bash
terraform apply -parallelism=20
```

### Targeted Operations

Update specific resources:

```bash
terraform apply -target=module.s3_bucket
```

## Version Control

### .gitignore

```
.terraform/
*.tfstate
*.tfstate.backup
*.tfvars
.terraform.lock.hcl
crash.log
override.tf
```

### Lock File

Commit `.terraform.lock.hcl` for reproducible builds

## Cost Optimization

### Resource Tagging

```hcl
resource "aws_s3_bucket" "logs" {
  bucket = var.bucket_name

  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    CostCenter  = var.cost_center
  }
}
```

### Default Tags

```hcl
provider "aws" {
  default_tags {
    tags = {
      ManagedBy = "Terraform"
      Project   = "S3-Log-Retention"
    }
  }
}
```

## Common Patterns

### Dynamic Blocks

```hcl
dynamic "transition" {
  for_each = var.transitions

  content {
    days          = transition.value.days
    storage_class = transition.value.storage_class
  }
}
```

### Conditional Resources

```hcl
resource "aws_cloudwatch_alarm" "optional" {
  count = var.enable_monitoring ? 1 : 0
  
  alarm_name = "example-alarm"
  # ...
}
```

### For Each

```hcl
resource "aws_s3_bucket" "logs" {
  for_each = toset(var.bucket_names)
  
  bucket = each.key
}
```

## Troubleshooting

### Debugging

```bash
export TF_LOG=DEBUG
terraform apply
```

### State Operations

```bash
# List resources
terraform state list

# Show resource
terraform state show aws_s3_bucket.logs

# Move resource
terraform state mv aws_s3_bucket.old aws_s3_bucket.new

# Remove from state
terraform state rm aws_s3_bucket.removed
```

## Checklist

- [ ] Use remote state backend
- [ ] Enable state locking
- [ ] Validate variables
- [ ] Mark sensitive outputs
- [ ] Use lifecycle meta-arguments appropriately
- [ ] Never commit sensitive data
- [ ] Format code before committing
- [ ] Validate configuration
- [ ] Review plan before applying
- [ ] Tag all resources
- [ ] Document modules
- [ ] Use versioning for modules
- [ ] Test in dev before prod
