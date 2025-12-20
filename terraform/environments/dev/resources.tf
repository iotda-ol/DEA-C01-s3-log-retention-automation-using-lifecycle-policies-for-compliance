# Local variables
locals {
  bucket_name        = "${var.bucket_prefix}-${var.environment}-${data.aws_caller_identity.current.account_id}"
  access_logs_bucket = "${var.bucket_prefix}-access-logs-${var.environment}-${data.aws_caller_identity.current.account_id}"
}

# Data sources
data "aws_caller_identity" "current" {}

# Access logs bucket (if logging enabled)
module "access_logs_bucket" {
  count  = var.enable_logging ? 1 : 0
  source = "../../modules/s3-bucket"

  bucket_name           = local.access_logs_bucket
  environment           = var.environment
  enable_versioning     = false
  enable_encryption     = true
  encryption_algorithm  = var.encryption_algorithm
  enable_logging        = false
  block_public_access   = true
  force_destroy         = false

  tags = var.tags
}

# Main log storage bucket
module "log_bucket" {
  source = "../../modules/s3-bucket"

  bucket_name          = local.bucket_name
  environment          = var.environment
  enable_versioning    = var.enable_versioning
  enable_encryption    = var.enable_encryption
  encryption_algorithm = var.encryption_algorithm
  enable_logging       = var.enable_logging
  logging_bucket       = var.enable_logging ? module.access_logs_bucket[0].bucket_id : null
  block_public_access  = true
  force_destroy        = false
  mfa_delete           = var.enable_mfa_delete

  tags = var.tags
}

# Lifecycle policy
module "lifecycle_policy" {
  source = "../../modules/lifecycle-policy"

  bucket_id                     = module.log_bucket.bucket_id
  retention_days                = var.retention_days
  enable_ia_transition          = var.enable_ia_transition
  ia_transition_days            = var.ia_transition_days
  enable_glacier_transition     = var.enable_glacier_transition
  glacier_transition_days       = var.glacier_transition_days
  enable_deep_archive_transition = var.enable_deep_archive
  cleanup_incomplete_uploads    = true
  incomplete_upload_days        = 7
}

# IAM role for S3 access
module "s3_access_role" {
  source = "../../modules/iam"

  role_name      = "s3-log-access-${var.environment}"
  services       = ["ec2.amazonaws.com", "lambda.amazonaws.com"]
  bucket_arns    = [module.log_bucket.bucket_arn]
  enable_read    = true
  enable_write   = true
  enable_delete  = false
  enable_lifecycle = true

  tags = var.tags
}
