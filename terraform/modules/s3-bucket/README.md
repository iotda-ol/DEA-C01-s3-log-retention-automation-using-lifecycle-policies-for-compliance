# S3 Bucket Module

This module creates a secure S3 bucket configured for log storage with best practices.

## Features

- Server-side encryption (AES256 or KMS)
- Versioning support
- Public access blocking
- Access logging capability
- Bucket ownership controls

## Usage

```hcl
module "log_bucket" {
  source = "./modules/s3-bucket"

  bucket_name        = "my-log-bucket-${var.environment}"
  enable_versioning  = true
  kms_key_id         = aws_kms_key.log_key.id
  access_log_bucket  = "my-access-log-bucket"
  
  tags = {
    Environment = "production"
    Team        = "platform"
  }
}
```

## Variables

See `variables.tf` for all configurable options.

## Outputs

- `bucket_id` - The name of the bucket
- `bucket_arn` - The ARN of the bucket
- `bucket_region` - The AWS region where the bucket resides
- `bucket_domain_name` - The bucket domain name
