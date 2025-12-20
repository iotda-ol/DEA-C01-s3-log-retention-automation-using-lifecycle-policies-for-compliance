# IAM Module

This module creates IAM roles and policies for S3 log retention automation.

## Features

- S3 access roles with least privilege
- Cross-account access support
- Service-specific roles (Lambda, EC2, etc.)
- Policy attachments
- Assume role configurations

## Usage

```hcl
module "s3_access_role" {
  source = "../../modules/iam"

  role_name    = "s3-log-access"
  services     = ["ec2.amazonaws.com", "lambda.amazonaws.com"]
  bucket_arns  = [module.log_bucket.bucket_arn]
  enable_write = true
  enable_read  = true
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| role_name | Name of the IAM role | string | - | yes |
| services | AWS services that can assume the role | list(string) | - | yes |
| bucket_arns | ARNs of S3 buckets to grant access | list(string) | - | yes |
| enable_read | Enable read access to buckets | bool | true | no |
| enable_write | Enable write access to buckets | bool | false | no |
| enable_delete | Enable delete access to buckets | bool | false | no |
| enable_lifecycle | Enable lifecycle policy management | bool | true | no |
| tags | Additional tags | map(string) | {} | no |

## Outputs

| Name | Description |
|------|-------------|
| role_arn | ARN of the IAM role |
| role_name | Name of the IAM role |
| policy_arn | ARN of the IAM policy |
