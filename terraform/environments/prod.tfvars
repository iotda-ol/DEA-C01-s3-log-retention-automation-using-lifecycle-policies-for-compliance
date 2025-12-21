# Production Environment Configuration

aws_region        = "us-east-1"
environment       = "prod"
project_name      = "s3-log-retention"
log_bucket_name   = "prod-log-retention-bucket-12345"  # Change to unique name
retention_days    = 365
enable_versioning = true
enable_encryption = true
enable_monitoring = true
enable_access_logging = true
alarm_email       = "prod-alerts@example.com"

lifecycle_transitions = [
  {
    days          = 30
    storage_class = "STANDARD_IA"
  },
  {
    days          = 90
    storage_class = "GLACIER"
  },
  {
    days          = 180
    storage_class = "DEEP_ARCHIVE"
  }
]

default_tags = {
  Environment = "Production"
  ManagedBy   = "Terraform"
  Project     = "S3-Log-Retention"
  CostCenter  = "Operations"
  Compliance  = "Required"
}
