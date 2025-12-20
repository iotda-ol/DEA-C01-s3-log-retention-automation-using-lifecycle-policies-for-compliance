/**
 * S3 Bucket Module
 * Creates an S3 bucket with best practices for log retention
 */

resource "aws_s3_bucket" "log_bucket" {
  bucket = var.bucket_name

  tags = merge(
    var.tags,
    {
      Name        = var.bucket_name
      Purpose     = "Log Retention"
      Compliance  = "DEA-C01"
      ManagedBy   = "Terraform"
    }
  )
}

# Enable versioning for data protection
resource "aws_s3_bucket_versioning" "log_bucket_versioning" {
  bucket = aws_s3_bucket.log_bucket.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}

# Enable server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "log_bucket_encryption" {
  bucket = aws_s3_bucket.log_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = var.encryption_type
      kms_master_key_id = var.encryption_type == "aws:kms" ? var.kms_key_id : null
    }
    bucket_key_enabled = var.encryption_type == "aws:kms" ? true : false
  }
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "log_bucket_public_access_block" {
  bucket = aws_s3_bucket.log_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable bucket logging if configured
resource "aws_s3_bucket_logging" "log_bucket_logging" {
  count = var.enable_access_logging ? 1 : 0

  bucket = aws_s3_bucket.log_bucket.id

  target_bucket = var.access_log_bucket
  target_prefix = var.access_log_prefix
}

# Configure bucket ownership controls
resource "aws_s3_bucket_ownership_controls" "log_bucket_ownership" {
  bucket = aws_s3_bucket.log_bucket.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# Enable S3 inventory for tracking
resource "aws_s3_bucket_inventory" "log_bucket_inventory" {
  count = var.enable_inventory ? 1 : 0

  bucket = aws_s3_bucket.log_bucket.id
  name   = "${var.bucket_name}-inventory"

  included_object_versions = "All"

  schedule {
    frequency = var.inventory_frequency
  }

  destination {
    bucket {
      format     = var.inventory_format
      bucket_arn = var.inventory_destination_bucket != "" ? var.inventory_destination_bucket : aws_s3_bucket.log_bucket.arn
      prefix     = var.inventory_prefix
    }
  }

  optional_fields = [
    "Size",
    "LastModifiedDate",
    "StorageClass",
    "ETag",
    "IsMultipartUploaded",
    "ReplicationStatus",
    "EncryptionStatus"
  ]
}
