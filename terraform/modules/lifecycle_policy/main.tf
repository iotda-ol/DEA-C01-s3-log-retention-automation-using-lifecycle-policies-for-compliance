/**
 * Lifecycle Policy Module
 * Manages S3 lifecycle policies for automated log retention and compliance
 */

resource "aws_s3_bucket_lifecycle_configuration" "log_retention_policy" {
  bucket = var.bucket_id

  # Rule for standard log retention (1 year deletion)
  rule {
    id     = var.retention_rule_id
    status = var.retention_rule_enabled ? "Enabled" : "Disabled"

    # Apply to specific prefix if specified
    dynamic "filter" {
      for_each = var.log_prefix != "" ? [1] : []
      content {
        prefix = var.log_prefix
      }
    }

    # Transition to Intelligent-Tiering after configured days
    dynamic "transition" {
      for_each = var.enable_intelligent_tiering ? [1] : []
      content {
        days          = var.days_to_intelligent_tiering
        storage_class = "INTELLIGENT_TIERING"
      }
    }

    # Transition to Standard-IA after configured days
    dynamic "transition" {
      for_each = var.enable_standard_ia_transition ? [1] : []
      content {
        days          = var.days_to_standard_ia
        storage_class = "STANDARD_IA"
      }
    }

    # Transition to Glacier after configured days
    dynamic "transition" {
      for_each = var.enable_glacier_transition ? [1] : []
      content {
        days          = var.days_to_glacier
        storage_class = "GLACIER"
      }
    }

    # Transition to Glacier Deep Archive after configured days
    dynamic "transition" {
      for_each = var.enable_deep_archive_transition ? [1] : []
      content {
        days          = var.days_to_deep_archive
        storage_class = "DEEP_ARCHIVE"
      }
    }

    # Expire (delete) objects after retention period
    expiration {
      days = var.retention_days
    }

    # Handle noncurrent versions if versioning is enabled
    dynamic "noncurrent_version_transition" {
      for_each = var.manage_noncurrent_versions ? [1] : []
      content {
        noncurrent_days = var.noncurrent_version_transition_days
        storage_class   = var.noncurrent_version_storage_class
      }
    }

    dynamic "noncurrent_version_expiration" {
      for_each = var.manage_noncurrent_versions ? [1] : []
      content {
        noncurrent_days = var.noncurrent_version_expiration_days
      }
    }

    # Clean up incomplete multipart uploads
    abort_incomplete_multipart_upload {
      days_after_initiation = var.abort_incomplete_multipart_upload_days
    }
  }

  # Additional rule for different log types if configured
  dynamic "rule" {
    for_each = var.additional_rules
    content {
      id     = rule.value.id
      status = rule.value.enabled ? "Enabled" : "Disabled"

      dynamic "filter" {
        for_each = rule.value.prefix != "" ? [1] : []
        content {
          prefix = rule.value.prefix
        }
      }

      dynamic "transition" {
        for_each = rule.value.transitions
        content {
          days          = transition.value.days
          storage_class = transition.value.storage_class
        }
      }

      expiration {
        days = rule.value.expiration_days
      }
    }
  }
}
