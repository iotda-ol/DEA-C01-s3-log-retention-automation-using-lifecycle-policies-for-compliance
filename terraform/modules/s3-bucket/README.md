# S3 Bucket Module

This module creates a secure S3 bucket with best practices enabled.

## Features

- Encryption at rest (AES256 or KMS)
- Versioning support
- Public access blocking
- Server access logging
- Object lock support
- Lifecycle policies
- Cost allocation tags

## Usage

```hcl
module "log_bucket" {
  source = "../../modules/s3-bucket"

  bucket_name        = "my-log-bucket"
  environment        = "prod"
  enable_versioning  = true
  enable_encryption  = true
  enable_logging     = true
  
  tags = {
    Project    = "LogRetention"
    CostCenter = "IT"
  }
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | - | yes |
| environment | Environment name | string | "dev" | no |
| enable_versioning | Enable bucket versioning | bool | true | no |
| enable_encryption | Enable server-side encryption | bool | true | no |
| encryption_algorithm | SSE algorithm (AES256 or aws:kms) | string | "AES256" | no |
| kms_key_id | KMS key ID for encryption | string | null | no |
| enable_logging | Enable access logging | bool | true | no |
| logging_bucket | Target bucket for access logs | string | null | no |
| block_public_access | Block all public access | bool | true | no |
| force_destroy | Allow bucket deletion with objects | bool | false | no |
| tags | Additional tags | map(string) | {} | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | ID of the S3 bucket |
| bucket_arn | ARN of the S3 bucket |
| bucket_domain_name | Domain name of the bucket |
| bucket_regional_domain_name | Regional domain name |

## Examples

See the [examples](../../examples/) directory for more usage examples.
