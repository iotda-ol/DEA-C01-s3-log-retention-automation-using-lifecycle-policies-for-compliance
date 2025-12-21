/**
 * Basic Example - S3 Log Retention with Lifecycle Policy
 * This example demonstrates a simple S3 bucket with 1-year log retention
 */

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Create S3 bucket for log storage
module "log_bucket" {
  source = "../../modules/s3_bucket"

  bucket_name       = var.bucket_name
  enable_versioning = var.enable_versioning
  encryption_type   = var.encryption_type

  tags = var.tags
}

# Apply lifecycle policy for 1-year retention
module "lifecycle_policy" {
  source = "../../modules/lifecycle_policy"

  bucket_id                      = module.log_bucket.bucket_id
  retention_days                 = var.retention_days
  enable_standard_ia_transition  = true
  days_to_standard_ia           = 30
  enable_glacier_transition      = true
  days_to_glacier               = 90
  manage_noncurrent_versions    = true

  depends_on = [module.log_bucket]
}

# Create IAM role for log processing (optional)
module "iam" {
  source = "../../modules/iam"

  project_name       = var.project_name
  bucket_name        = var.bucket_name
  create_lambda_role = var.create_lambda_role

  tags = var.tags

  depends_on = [module.log_bucket]
}

# Set up monitoring and alerts
module "monitoring" {
  source = "../../modules/monitoring"

  bucket_name                = var.bucket_name
  enable_size_alarm          = var.enable_monitoring
  enable_object_count_alarm  = var.enable_monitoring
  enable_error_alarms        = var.enable_monitoring
  create_dashboard           = var.enable_monitoring

  tags = var.tags

  depends_on = [module.log_bucket]
}
