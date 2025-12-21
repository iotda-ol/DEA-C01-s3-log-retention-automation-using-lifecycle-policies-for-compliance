variable "bucket_name" {
  description = "Name of the S3 bucket to monitor"
  type        = string
}

variable "tags" {
  description = "Tags to apply to monitoring resources"
  type        = map(string)
  default     = {}
}

variable "enable_size_alarm" {
  description = "Enable CloudWatch alarm for bucket size"
  type        = bool
  default     = true
}

variable "size_alarm_threshold_bytes" {
  description = "Bucket size threshold in bytes for alarm"
  type        = number
  default     = 1099511627776 # 1 TB
}

variable "size_alarm_period" {
  description = "Period for bucket size metric (seconds)"
  type        = number
  default     = 86400 # 1 day
}

variable "size_alarm_evaluation_periods" {
  description = "Number of periods to evaluate for size alarm"
  type        = number
  default     = 1
}

variable "enable_object_count_alarm" {
  description = "Enable CloudWatch alarm for object count"
  type        = bool
  default     = true
}

variable "object_count_threshold" {
  description = "Object count threshold for alarm"
  type        = number
  default     = 1000000
}

variable "object_count_period" {
  description = "Period for object count metric (seconds)"
  type        = number
  default     = 86400 # 1 day
}

variable "object_count_evaluation_periods" {
  description = "Number of periods to evaluate for object count alarm"
  type        = number
  default     = 1
}

variable "enable_error_alarms" {
  description = "Enable CloudWatch alarms for S3 errors"
  type        = bool
  default     = true
}

variable "error_4xx_threshold" {
  description = "Threshold for 4xx errors"
  type        = number
  default     = 100
}

variable "error_5xx_threshold" {
  description = "Threshold for 5xx errors"
  type        = number
  default     = 10
}

variable "alarm_actions" {
  description = "List of ARNs to notify when alarm triggers"
  type        = list(string)
  default     = []
}

variable "create_dashboard" {
  description = "Create CloudWatch dashboard for monitoring"
  type        = bool
  default     = true
}

variable "create_sns_topic" {
  description = "Create SNS topic for alarm notifications"
  type        = bool
  default     = false
}

variable "alarm_email_endpoints" {
  description = "Email addresses to receive alarm notifications"
  type        = list(string)
  default     = []
}

variable "sns_kms_key_id" {
  description = "KMS key ID for SNS topic encryption"
  type        = string
  default     = ""
}

variable "create_log_group" {
  description = "Create CloudWatch log group for custom metrics"
  type        = bool
  default     = false
}

variable "log_retention_days" {
  description = "Retention period for CloudWatch logs"
  type        = number
  default     = 30
}

variable "cloudwatch_kms_key_id" {
  description = "KMS key ID for CloudWatch log encryption"
  type        = string
  default     = ""
}
