# Logging Module

This module sets up comprehensive monitoring and logging for S3 buckets.

## Features

- CloudWatch log groups for S3 events
- CloudWatch metric alarms for lifecycle failures
- Storage quota monitoring
- CloudTrail for data event tracking
- SNS notifications for alerts

## Usage

```hcl
module "logging" {
  source = "./modules/logging"

  bucket_name             = module.log_bucket.bucket_id
  bucket_arn              = module.log_bucket.bucket_arn
  cloudtrail_bucket_name  = "my-cloudtrail-bucket"
  alert_email             = "alerts@example.com"
  storage_quota_bytes     = 1099511627776 # 1TB
  
  alarm_actions = [module.logging.sns_topic_arn]

  tags = {
    Environment = "production"
  }
}
```

## Monitoring

- **Lifecycle Failures**: Alerts when 4xx errors exceed threshold
- **Storage Quota**: Alerts when bucket size exceeds configured limit
- **CloudTrail**: Tracks all S3 data events for audit

## Outputs

Exports all resource ARNs for integration with other systems.
