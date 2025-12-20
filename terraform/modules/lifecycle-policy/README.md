# Lifecycle Policy Module

This module manages S3 lifecycle policies for automated log retention and deletion.

## Features

- Multiple lifecycle rules support
- Transition to different storage classes (IA, Glacier, Deep Archive)
- Automatic expiration after specified days
- Noncurrent version management
- Incomplete multipart upload cleanup

## Usage

```hcl
module "lifecycle_policy" {
  source    = "./modules/lifecycle-policy"
  bucket_id = module.log_bucket.bucket_id

  lifecycle_rules = [
    {
      id      = "delete-old-logs"
      enabled = true
      prefix  = "logs/"
      transitions = [
        {
          days          = 30
          storage_class = "STANDARD_IA"
        },
        {
          days          = 90
          storage_class = "GLACIER"
        }
      ]
      expiration_days = 365
      abort_incomplete_days = 7
    }
  ]
}
```

## Compliance

Supports DEA-C01 compliance requirements for:
- 1-year log retention
- Automatic deletion for compliance
- Cost optimization through storage class transitions
