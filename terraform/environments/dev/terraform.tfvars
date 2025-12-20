# Development Environment Configuration

environment      = "dev"
aws_region       = "us-east-1"
retention_days   = 365
bucket_prefix    = "dev-logs"

# Storage transitions
enable_ia_transition       = true
ia_transition_days         = 30
enable_glacier_transition  = true
glacier_transition_days    = 90
enable_deep_archive        = false

# Security
enable_versioning    = true
enable_encryption    = true
encryption_algorithm = "AES256"
enable_mfa_delete    = false

# Monitoring
enable_logging          = true
enable_cloudwatch_alarm = true

# Tags
tags = {
  Environment = "Development"
  Project     = "S3LogRetention"
  ManagedBy   = "Terraform"
  CostCenter  = "IT-Dev"
  Owner       = "DevOps"
}
