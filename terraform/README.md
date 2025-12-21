# Terraform Modules

This directory contains reusable Terraform modules for S3 log retention automation.

## Available Modules

### S3 Bucket Module

**Path**: `modules/s3_bucket/`

Creates an S3 bucket with best practices for log storage:
- Server-side encryption (AES256 or KMS)
- Versioning support
- Public access blocking
- Optional access logging
- S3 Inventory tracking

**Usage**:
```hcl
module "log_bucket" {
  source = "./modules/s3_bucket"

  bucket_name       = "my-log-bucket"
  enable_versioning = true
  encryption_type   = "AES256"
  
  tags = {
    Environment = "production"
    Purpose     = "LogRetention"
  }
}
```

### Lifecycle Policy Module

**Path**: `modules/lifecycle_policy/`

Manages S3 lifecycle policies for automated retention:
- Configurable retention periods
- Multi-tier transitions
- Noncurrent version management
- Multipart upload cleanup

**Usage**:
```hcl
module "lifecycle_policy" {
  source = "./modules/lifecycle_policy"

  bucket_id                     = module.log_bucket.bucket_id
  retention_days                = 365
  enable_standard_ia_transition = true
  days_to_standard_ia          = 30
  enable_glacier_transition     = true
  days_to_glacier              = 90
}
```

### IAM Module

**Path**: `modules/iam/`

Creates IAM roles and policies:
- Lambda execution roles
- EventBridge permissions
- S3 inventory roles
- Cross-account access

**Usage**:
```hcl
module "iam" {
  source = "./modules/iam"

  project_name       = "log-retention"
  bucket_name        = module.log_bucket.bucket_id
  create_lambda_role = true
  
  tags = {
    Environment = "production"
  }
}
```

### Monitoring Module

**Path**: `modules/monitoring/`

Sets up CloudWatch monitoring:
- Bucket size alarms
- Object count alarms
- Error rate alarms
- Custom dashboards
- SNS notifications

**Usage**:
```hcl
module "monitoring" {
  source = "./modules/monitoring"

  bucket_name                = module.log_bucket.bucket_id
  enable_size_alarm          = true
  enable_object_count_alarm  = true
  enable_error_alarms        = true
  create_dashboard           = true
  
  tags = {
    Environment = "production"
  }
}
```

## Module Composition

Modules are designed to be composable. Use them together for complete infrastructure:

```hcl
# Create bucket
module "log_bucket" {
  source = "./modules/s3_bucket"
  # ... configuration
}

# Apply lifecycle policy
module "lifecycle_policy" {
  source    = "./modules/lifecycle_policy"
  bucket_id = module.log_bucket.bucket_id
  # ... configuration
}

# Set up IAM
module "iam" {
  source      = "./modules/iam"
  bucket_name = module.log_bucket.bucket_id
  # ... configuration
}

# Configure monitoring
module "monitoring" {
  source      = "./modules/monitoring"
  bucket_name = module.log_bucket.bucket_id
  # ... configuration
}
```

## Best Practices

1. **Variables**: Always use variables for configuration
2. **Outputs**: Export important values for other modules
3. **Validation**: Include validation rules in variables
4. **Documentation**: Add comments for complex logic
5. **Versioning**: Pin module versions in production

## Examples

See the `examples/` directory for complete working examples:
- `examples/basic/`: Basic deployment
- `examples/advanced/`: Advanced features
- `examples/multi_bucket/`: Multiple buckets
