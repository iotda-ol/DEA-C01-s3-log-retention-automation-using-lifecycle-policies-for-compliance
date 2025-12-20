# Lifecycle Policy Module

This module manages S3 lifecycle policies for automated object transitions and expirations.

## Features

- Automatic transitions between storage classes
- Configurable expiration policies
- Support for multiple lifecycle rules
- Prefix and tag-based filtering
- Incomplete multipart upload cleanup
- Noncurrent version management

## Usage

```hcl
module "lifecycle_policy" {
  source = "../../modules/lifecycle-policy"

  bucket_id      = module.s3_bucket.bucket_id
  retention_days = 365

  enable_glacier_transition = true
  glacier_transition_days   = 90

  enable_ia_transition = true
  ia_transition_days   = 30
}
```

## Compliance-Focused Example

```hcl
module "compliance_lifecycle" {
  source = "../../modules/lifecycle-policy"

  bucket_id      = "my-compliance-logs"
  retention_days = 365  # 1 year retention

  enable_ia_transition      = true
  ia_transition_days        = 30

  enable_glacier_transition = true
  glacier_transition_days   = 90

  prefix = "logs/"
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_id | S3 bucket ID | string | - | yes |
| retention_days | Days to retain objects before deletion | number | 365 | no |
| enable_ia_transition | Enable transition to STANDARD_IA | bool | false | no |
| ia_transition_days | Days before transition to IA | number | 30 | no |
| enable_glacier_transition | Enable transition to GLACIER | bool | false | no |
| glacier_transition_days | Days before transition to Glacier | number | 90 | no |
| enable_deep_archive_transition | Enable transition to DEEP_ARCHIVE | bool | false | no |
| deep_archive_transition_days | Days before deep archive | number | 180 | no |
| prefix | Object prefix filter | string | "" | no |
| tags | Object tags filter | map(string) | {} | no |
| cleanup_incomplete_uploads | Enable cleanup of incomplete multipart uploads | bool | true | no |
| incomplete_upload_days | Days before cleaning incomplete uploads | number | 7 | no |

## Outputs

| Name | Description |
|------|-------------|
| lifecycle_rule_ids | List of lifecycle rule IDs |

## Cost Optimization

This module helps optimize costs by:
1. Moving old data to cheaper storage classes
2. Automatically deleting expired data
3. Cleaning up incomplete multipart uploads
4. Managing noncurrent object versions
