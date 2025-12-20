# S3 Bucket for Log Storage with Lifecycle Policies
resource "aws_s3_bucket" "log_bucket" {
  bucket = var.bucket_name

  tags = merge(
    var.tags,
    {
      Name = var.bucket_name
    }
  )
}

# Enable versioning for data protection
resource "aws_s3_bucket_versioning" "log_bucket_versioning" {
  bucket = aws_s3_bucket.log_bucket.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Disabled"
  }
}

# Configure server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "log_bucket_encryption" {
  bucket = aws_s3_bucket.log_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = var.kms_key_id != null ? "aws:kms" : "AES256"
      kms_master_key_id = var.kms_key_id
    }
    bucket_key_enabled = var.kms_key_id != null ? true : false
  }
}

# Block all public access to the bucket
resource "aws_s3_bucket_public_access_block" "log_bucket_public_access_block" {
  bucket = aws_s3_bucket.log_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Configure S3 Lifecycle Policy for automated log retention and cost optimization
resource "aws_s3_bucket_lifecycle_configuration" "log_bucket_lifecycle" {
  bucket = aws_s3_bucket.log_bucket.id

  # Rule for standard log objects
  rule {
    id     = "log-retention-policy"
    status = "Enabled"

    # Apply to all objects in the bucket
    filter {}

    # Transition to Infrequent Access after 90 days for cost optimization
    transition {
      days          = var.transition_to_ia_days
      storage_class = "STANDARD_IA"
    }

    # Transition to Glacier for long-term archival before deletion
    transition {
      days          = var.transition_to_glacier_days
      storage_class = "GLACIER"
    }

    # Automatically delete objects after retention period (365 days for 1 year)
    expiration {
      days = var.retention_days
    }
  }

  # Rule for versioned objects (if versioning is enabled)
  rule {
    id     = "cleanup-old-versions"
    status = "Enabled"

    # Apply to all objects in the bucket
    filter {}

    noncurrent_version_transition {
      noncurrent_days = var.noncurrent_transition_days
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = var.noncurrent_expiration_days
    }
  }

  # Rule for cleaning up incomplete multipart uploads
  rule {
    id     = "cleanup-incomplete-uploads"
    status = "Enabled"

    # Apply to all objects in the bucket
    filter {}

    abort_incomplete_multipart_upload {
      days_after_initiation = var.multipart_cleanup_days
    }
  }
}

# Note: S3 access logging is commented out to avoid recursive logging loop.
# To enable access logging, follow these steps:
# 1. Create a separate S3 bucket for access logs
# 2. Add a variable for the access logs bucket name in variables.tf
# 3. Uncomment and configure the resource below
#
# Example configuration:
# resource "aws_s3_bucket_logging" "log_bucket_access_logging" {
#   bucket = aws_s3_bucket.log_bucket.id
#
#   target_bucket = var.access_logs_bucket_name  # Set this to your access logs bucket
#   target_prefix = "access-logs/${var.bucket_name}/"
# }

# IAM Policy Document for least-privilege log writing
data "aws_iam_policy_document" "log_writer_policy" {
  statement {
    sid    = "AllowLogWriting"
    effect = "Allow"

    actions = [
      "s3:PutObject",
      "s3:PutObjectAcl"
    ]

    resources = [
      "${aws_s3_bucket.log_bucket.arn}/*"
    ]
  }

  statement {
    sid    = "AllowBucketListing"
    effect = "Allow"

    actions = [
      "s3:ListBucket"
    ]

    resources = [
      aws_s3_bucket.log_bucket.arn
    ]
  }
}

# IAM Policy for log writers (can be attached to roles or users)
resource "aws_iam_policy" "log_writer_policy" {
  name        = "${var.bucket_name}-log-writer-policy"
  description = "Least-privilege policy for writing logs to S3 bucket"
  policy      = data.aws_iam_policy_document.log_writer_policy.json

  tags = var.tags
}

# Example IAM Role for EC2 instances or applications to write logs
resource "aws_iam_role" "log_writer_role" {
  name = "${var.bucket_name}-log-writer-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = [
            "ec2.amazonaws.com",
            "lambda.amazonaws.com",
            "ecs-tasks.amazonaws.com"
          ]
        }
      }
    ]
  })

  tags = var.tags
}

# Attach the log writer policy to the role
resource "aws_iam_role_policy_attachment" "log_writer_role_attachment" {
  role       = aws_iam_role.log_writer_role.name
  policy_arn = aws_iam_policy.log_writer_policy.arn
}

# Instance profile for EC2 instances (if needed)
resource "aws_iam_instance_profile" "log_writer_instance_profile" {
  name = "${var.bucket_name}-log-writer-profile"
  role = aws_iam_role.log_writer_role.name

  tags = var.tags
}
