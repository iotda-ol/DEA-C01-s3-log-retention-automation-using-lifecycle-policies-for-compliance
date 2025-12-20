# IAM Module

This module creates IAM roles and policies for S3 log management operations.

## Features

- Log writer role for applications to write logs
- Log reader role for analysis and compliance checking
- Lifecycle manager role for policy management
- Configurable assume role policies
- Least privilege access policies

## Usage

```hcl
module "iam" {
  source = "./modules/iam"

  name_prefix    = "my-app"
  log_bucket_arn = module.log_bucket.bucket_arn

  log_writer_assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })

  tags = {
    Environment = "production"
  }
}
```

## Outputs

All role ARNs and names are exported for use in other modules.
