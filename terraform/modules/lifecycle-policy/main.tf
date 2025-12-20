# Lifecycle Policy Module

resource "aws_s3_bucket_lifecycle_configuration" "log_retention" {
  bucket = var.bucket_name

  rule {
    id     = "log-retention-policy"
    status = "Enabled"

    filter {
      prefix = var.prefix
    }

    # Transitions to different storage classes
    dynamic "transition" {
      for_each = var.transitions

      content {
        days          = transition.value.days
        storage_class = transition.value.storage_class
      }
    }

    # Expiration rule
    expiration {
      days = var.retention_days
    }

    # Cleanup incomplete multipart uploads
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  # Rule for noncurrent versions (if versioning is enabled)
  dynamic "rule" {
    for_each = var.enable_noncurrent_version_expiration ? [1] : []

    content {
      id     = "noncurrent-version-cleanup"
      status = "Enabled"

      noncurrent_version_expiration {
        noncurrent_days = var.noncurrent_version_retention_days
      }
    }
  }
}
