locals {
  # Build transitions list dynamically based on enabled options
  transitions = concat(
    var.enable_ia_transition ? [
      {
        days          = var.ia_transition_days
        storage_class = "STANDARD_IA"
      }
    ] : [],
    var.enable_glacier_transition ? [
      {
        days          = var.glacier_transition_days
        storage_class = "GLACIER"
      }
    ] : [],
    var.enable_deep_archive_transition ? [
      {
        days          = var.deep_archive_transition_days
        storage_class = "DEEP_ARCHIVE"
      }
    ] : []
  )

  # Build noncurrent version transitions
  noncurrent_transitions = var.enable_noncurrent_version_transitions ? concat(
    var.enable_glacier_transition ? [
      {
        noncurrent_days = var.glacier_transition_days
        storage_class   = "GLACIER"
      }
    ] : []
  ) : []
}

resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = var.bucket_id

  # Main expiration rule
  rule {
    id     = "retention-policy"
    status = "Enabled"

    dynamic "filter" {
      for_each = var.prefix != "" || length(var.tags) > 0 ? [1] : []
      content {
        and {
          prefix = var.prefix
          tags   = var.tags
        }
      }
    }

    # Transitions
    dynamic "transition" {
      for_each = local.transitions
      content {
        days          = transition.value.days
        storage_class = transition.value.storage_class
      }
    }

    # Expiration
    expiration {
      days = var.retention_days
    }

    # Noncurrent version transitions
    dynamic "noncurrent_version_transition" {
      for_each = local.noncurrent_transitions
      content {
        noncurrent_days = noncurrent_version_transition.value.noncurrent_days
        storage_class   = noncurrent_version_transition.value.storage_class
      }
    }

    # Noncurrent version expiration
    noncurrent_version_expiration {
      noncurrent_days = var.noncurrent_version_expiration_days
    }
  }

  # Cleanup incomplete multipart uploads
  dynamic "rule" {
    for_each = var.cleanup_incomplete_uploads ? [1] : []
    content {
      id     = "cleanup-incomplete-uploads"
      status = "Enabled"

      abort_incomplete_multipart_upload {
        days_after_initiation = var.incomplete_upload_days
      }
    }
  }
}
