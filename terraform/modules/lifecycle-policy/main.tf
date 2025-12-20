/**
 * S3 Lifecycle Policy Module
 * Manages lifecycle policies for automated log retention and deletion
 */

resource "aws_s3_bucket_lifecycle_configuration" "log_lifecycle" {
  bucket = var.bucket_id

  dynamic "rule" {
    for_each = var.lifecycle_rules
    content {
      id     = rule.value.id
      status = rule.value.enabled ? "Enabled" : "Disabled"

      filter {
        and {
          prefix = lookup(rule.value, "prefix", "")
          tags   = lookup(rule.value, "tags", {})
        }
      }

      dynamic "transition" {
        for_each = lookup(rule.value, "transitions", [])
        content {
          days          = transition.value.days
          storage_class = transition.value.storage_class
        }
      }

      dynamic "expiration" {
        for_each = lookup(rule.value, "expiration_days", null) != null ? [1] : []
        content {
          days = rule.value.expiration_days
        }
      }

      dynamic "noncurrent_version_transition" {
        for_each = lookup(rule.value, "noncurrent_transitions", [])
        content {
          noncurrent_days = noncurrent_version_transition.value.days
          storage_class   = noncurrent_version_transition.value.storage_class
        }
      }

      dynamic "noncurrent_version_expiration" {
        for_each = lookup(rule.value, "noncurrent_expiration_days", null) != null ? [1] : []
        content {
          noncurrent_days = rule.value.noncurrent_expiration_days
        }
      }

      dynamic "abort_incomplete_multipart_upload" {
        for_each = lookup(rule.value, "abort_incomplete_days", null) != null ? [1] : []
        content {
          days_after_initiation = rule.value.abort_incomplete_days
        }
      }
    }
  }
}
