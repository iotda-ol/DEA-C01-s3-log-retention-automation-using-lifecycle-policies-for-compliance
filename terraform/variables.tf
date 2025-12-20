variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "dea-c01-log-retention"
}

variable "enable_versioning" {
  description = "Enable S3 bucket versioning"
  type        = bool
  default     = true
}

variable "enable_kms_encryption" {
  description = "Enable KMS encryption for S3 bucket"
  type        = bool
  default     = true
}

variable "kms_deletion_window_days" {
  description = "KMS key deletion window in days"
  type        = number
  default     = 30
}

variable "lifecycle_rules" {
  description = "Lifecycle rules for S3 bucket"
  type = list(object({
    id          = string
    enabled     = bool
    prefix      = optional(string)
    tags        = optional(map(string))
    transitions = optional(list(object({
      days          = number
      storage_class = string
    })))
    expiration_days = optional(number)
    noncurrent_transitions = optional(list(object({
      days          = number
      storage_class = string
    })))
    noncurrent_expiration_days = optional(number)
    abort_incomplete_days      = optional(number)
  }))
  default = [
    {
      id      = "default-log-retention"
      enabled = true
      prefix  = ""
      transitions = [
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
      expiration_days       = 365
      abort_incomplete_days = 7
    }
  ]
}

variable "log_writer_service_principals" {
  description = "AWS service principals allowed to write logs"
  type        = list(string)
  default     = ["ec2.amazonaws.com", "lambda.amazonaws.com"]
}

variable "log_reader_service_principals" {
  description = "AWS service principals allowed to read logs"
  type        = list(string)
  default     = ["lambda.amazonaws.com"]
}

variable "cloudtrail_bucket_name" {
  description = "S3 bucket for CloudTrail logs"
  type        = string
  default     = ""
}

variable "alert_email" {
  description = "Email for alert notifications"
  type        = string
  default     = ""
}

variable "storage_quota_bytes" {
  description = "Storage quota in bytes for alerts"
  type        = number
  default     = 1099511627776 # 1TB
}

variable "enable_sns_alerts" {
  description = "Enable SNS alerts"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags for resources"
  type        = map(string)
  default     = {}
}
