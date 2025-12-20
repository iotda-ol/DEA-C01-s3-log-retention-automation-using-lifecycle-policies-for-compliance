/**
 * Main Terraform Configuration
 * Orchestrates all modules for S3 log retention automation
 */

# S3 Bucket for logs
module "log_bucket" {
  source = "./modules/s3-bucket"

  bucket_name       = "${var.project_name}-logs-${var.environment}-${data.aws_caller_identity.current.account_id}"
  enable_versioning = var.enable_versioning
  kms_key_id        = var.enable_kms_encryption ? aws_kms_key.log_encryption[0].id : ""

  tags = var.tags
}

# Lifecycle Policies
module "lifecycle_policy" {
  source = "./modules/lifecycle-policy"

  bucket_id = module.log_bucket.bucket_id

  lifecycle_rules = var.lifecycle_rules
}

# IAM Roles and Policies
module "iam" {
  source = "./modules/iam"

  name_prefix    = "${var.project_name}-${var.environment}"
  log_bucket_arn = module.log_bucket.bucket_arn

  log_writer_assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = var.log_writer_service_principals
      }
    }]
  })

  log_reader_assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = var.log_reader_service_principals
      }
    }]
  })

  lifecycle_manager_assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = ["lambda.amazonaws.com"]
      }
    }]
  })

  tags = var.tags
}

# Logging and Monitoring
module "logging" {
  source = "./modules/logging"

  bucket_name            = module.log_bucket.bucket_id
  bucket_arn             = module.log_bucket.bucket_arn
  cloudtrail_bucket_name = var.cloudtrail_bucket_name
  alert_email            = var.alert_email
  storage_quota_bytes    = var.storage_quota_bytes
  
  alarm_actions = var.enable_sns_alerts ? [module.logging.sns_topic_arn] : []

  tags = var.tags
}

# KMS Key for encryption (optional)
resource "aws_kms_key" "log_encryption" {
  count = var.enable_kms_encryption ? 1 : 0

  description             = "KMS key for ${var.project_name} log encryption"
  deletion_window_in_days = var.kms_deletion_window_days
  enable_key_rotation     = true

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-log-encryption-${var.environment}"
    }
  )
}

resource "aws_kms_alias" "log_encryption" {
  count = var.enable_kms_encryption ? 1 : 0

  name          = "alias/${var.project_name}-log-encryption-${var.environment}"
  target_key_id = aws_kms_key.log_encryption[0].key_id
}

# Data source for current AWS account
data "aws_caller_identity" "current" {}
