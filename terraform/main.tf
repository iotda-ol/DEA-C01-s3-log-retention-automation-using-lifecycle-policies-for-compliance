# S3 Log Retention Automation - Main Configuration

locals {
  name_prefix = "${var.project_name}-${var.environment}"
  
  common_tags = merge(
    var.default_tags,
    {
      Environment = var.environment
      Name        = local.name_prefix
    }
  )
}

# S3 Bucket for log storage
module "s3_bucket" {
  source = "./modules/s3-bucket"

  bucket_name         = var.log_bucket_name
  enable_versioning   = var.enable_versioning
  enable_encryption   = var.enable_encryption
  enable_access_logging = var.enable_access_logging
  
  tags = local.common_tags
}

# Lifecycle policy for log retention
module "lifecycle_policy" {
  source = "./modules/lifecycle-policy"

  bucket_name        = module.s3_bucket.bucket_id
  retention_days     = var.retention_days
  transitions        = var.lifecycle_transitions
  
  tags = local.common_tags
}

# IAM role and policies
module "iam" {
  source = "./modules/iam"

  name_prefix = local.name_prefix
  bucket_arn  = module.s3_bucket.bucket_arn
  
  tags = local.common_tags
}

# CloudWatch monitoring (optional)
module "cloudwatch" {
  count  = var.enable_monitoring ? 1 : 0
  source = "./modules/cloudwatch"

  name_prefix   = local.name_prefix
  bucket_name   = module.s3_bucket.bucket_id
  sns_topic_arn = var.alarm_email != "" ? module.sns[0].topic_arn : null
  
  tags = local.common_tags
}

# SNS topic for alerts (optional)
module "sns" {
  count  = var.enable_monitoring && var.alarm_email != "" ? 1 : 0
  source = "./modules/sns"

  name_prefix = local.name_prefix
  email       = var.alarm_email
  
  tags = local.common_tags
}
