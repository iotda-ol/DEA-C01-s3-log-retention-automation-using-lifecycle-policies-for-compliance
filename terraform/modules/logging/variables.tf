variable "bucket_name" {
  description = "Name of the S3 bucket to monitor"
  type        = string
}

variable "bucket_arn" {
  description = "ARN of the S3 bucket to monitor"
  type        = string
}

variable "enable_cloudwatch_logging" {
  description = "Enable CloudWatch logging for S3 events"
  type        = bool
  default     = true
}

variable "cloudwatch_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 365
}

variable "enable_lifecycle_monitoring" {
  description = "Enable CloudWatch alarms for lifecycle policy monitoring"
  type        = bool
  default     = true
}

variable "enable_storage_monitoring" {
  description = "Enable CloudWatch alarms for storage monitoring"
  type        = bool
  default     = true
}

variable "storage_quota_bytes" {
  description = "Storage quota threshold in bytes for alerts"
  type        = number
  default     = 1099511627776 # 1TB
}

variable "alarm_actions" {
  description = "List of ARNs to notify when alarm triggers"
  type        = list(string)
  default     = []
}

variable "enable_cloudtrail" {
  description = "Enable CloudTrail for S3 data events"
  type        = bool
  default     = true
}

variable "cloudtrail_bucket_name" {
  description = "S3 bucket name for CloudTrail logs"
  type        = string
  default     = ""
}

variable "cloudtrail_multi_region" {
  description = "Enable multi-region CloudTrail"
  type        = bool
  default     = false
}

variable "create_sns_topic" {
  description = "Create SNS topic for alerts"
  type        = bool
  default     = true
}

variable "alert_email" {
  description = "Email address for alert notifications"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags to apply to logging resources"
  type        = map(string)
  default     = {}
}
