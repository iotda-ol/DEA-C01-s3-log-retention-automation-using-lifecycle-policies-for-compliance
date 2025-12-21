variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "bucket_name" {
  description = "Name of the S3 bucket to monitor"
  type        = string
}

variable "sns_topic_arn" {
  description = "ARN of SNS topic for alarms"
  type        = string
  default     = null
}

variable "bucket_size_threshold" {
  description = "Threshold for bucket size alarm (bytes)"
  type        = number
  default     = 1099511627776 # 1 TB
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
