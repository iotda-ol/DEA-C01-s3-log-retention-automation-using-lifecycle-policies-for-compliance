# Staging Environment Configuration

aws_region        = "us-east-1"
environment       = "staging"
project_name      = "s3-log-retention"
log_bucket_name   = "staging-log-retention-bucket-12345"  # Change to unique name
retention_days    = 180
enable_versioning = true
enable_encryption = true
enable_monitoring = true
alarm_email       = "alerts@example.com"

lifecycle_transitions = [
  {
    days          = 30
    storage_class = "STANDARD_IA"
  },
  {
    days          = 90
    storage_class = "GLACIER"
  }
]

default_tags = {
  Environment = "Staging"
  ManagedBy   = "Terraform"
  Project     = "S3-Log-Retention"
  CostCenter  = "Engineering"
}
