# Development Environment Configuration

aws_region        = "us-east-1"
environment       = "dev"
project_name      = "s3-log-retention"
log_bucket_name   = "dev-log-retention-bucket-12345"  # Change to unique name
retention_days    = 90
enable_versioning = true
enable_encryption = true
enable_monitoring = true

lifecycle_transitions = [
  {
    days          = 30
    storage_class = "STANDARD_IA"
  }
]

default_tags = {
  Environment = "Development"
  ManagedBy   = "Terraform"
  Project     = "S3-Log-Retention"
  CostCenter  = "Engineering"
}
