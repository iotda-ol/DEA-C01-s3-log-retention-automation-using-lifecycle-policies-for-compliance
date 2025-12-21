variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "s3-log-retention"
}

variable "log_bucket_name" {
  description = "Name of the S3 bucket for log storage"
  type        = string
}

variable "retention_days" {
  description = "Number of days to retain logs"
  type        = number
  default     = 365
}

variable "enable_versioning" {
  description = "Enable S3 bucket versioning"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Enable S3 bucket encryption"
  type        = bool
  default     = true
}

variable "enable_access_logging" {
  description = "Enable S3 access logging"
  type        = bool
  default     = true
}

variable "lifecycle_transitions" {
  description = "Lifecycle transition rules"
  type = list(object({
    days          = number
    storage_class = string
  }))
  default = [
    {
      days          = 30
      storage_class = "STANDARD_IA"
    },
    {
      days          = 90
      storage_class = "GLACIER"
    }
  ]
}

variable "default_tags" {
  description = "Default tags to apply to all resources"
  type        = map(string)
  default = {
    ManagedBy = "Terraform"
    Project   = "S3-Log-Retention"
  }
}

variable "enable_monitoring" {
  description = "Enable CloudWatch monitoring"
  type        = bool
  default     = true
}

variable "alarm_email" {
  description = "Email address for CloudWatch alarms"
  type        = string
  default     = ""
}
