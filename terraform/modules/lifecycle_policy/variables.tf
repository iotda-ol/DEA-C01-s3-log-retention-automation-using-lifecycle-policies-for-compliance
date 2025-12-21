variable "bucket_id" {
  description = "ID of the S3 bucket to apply lifecycle policy"
  type        = string
}

variable "retention_rule_id" {
  description = "Unique identifier for the retention rule"
  type        = string
  default     = "log-retention-rule"
}

variable "retention_rule_enabled" {
  description = "Enable or disable the retention rule"
  type        = bool
  default     = true
}

variable "log_prefix" {
  description = "Prefix filter for logs (empty string applies to all objects)"
  type        = string
  default     = ""
}

variable "retention_days" {
  description = "Number of days to retain logs before deletion (compliance requirement: 365 days)"
  type        = number
  default     = 365
  validation {
    condition     = var.retention_days > 0 && var.retention_days <= 3650
    error_message = "Retention days must be between 1 and 3650 (10 years)"
  }
}

variable "enable_intelligent_tiering" {
  description = "Enable transition to Intelligent-Tiering storage class"
  type        = bool
  default     = false
}

variable "days_to_intelligent_tiering" {
  description = "Days before transitioning to Intelligent-Tiering"
  type        = number
  default     = 30
}

variable "enable_standard_ia_transition" {
  description = "Enable transition to Standard-IA storage class"
  type        = bool
  default     = true
}

variable "days_to_standard_ia" {
  description = "Days before transitioning to Standard-IA"
  type        = number
  default     = 30
}

variable "enable_glacier_transition" {
  description = "Enable transition to Glacier storage class"
  type        = bool
  default     = true
}

variable "days_to_glacier" {
  description = "Days before transitioning to Glacier"
  type        = number
  default     = 90
}

variable "enable_deep_archive_transition" {
  description = "Enable transition to Glacier Deep Archive storage class"
  type        = bool
  default     = false
}

variable "days_to_deep_archive" {
  description = "Days before transitioning to Deep Archive"
  type        = number
  default     = 180
}

variable "manage_noncurrent_versions" {
  description = "Manage lifecycle of noncurrent object versions"
  type        = bool
  default     = true
}

variable "noncurrent_version_transition_days" {
  description = "Days before transitioning noncurrent versions"
  type        = number
  default     = 30
}

variable "noncurrent_version_storage_class" {
  description = "Storage class for noncurrent versions"
  type        = string
  default     = "GLACIER"
}

variable "noncurrent_version_expiration_days" {
  description = "Days before expiring noncurrent versions"
  type        = number
  default     = 90
}

variable "abort_incomplete_multipart_upload_days" {
  description = "Days to abort incomplete multipart uploads"
  type        = number
  default     = 7
}

variable "additional_rules" {
  description = "Additional lifecycle rules for different log types"
  type = list(object({
    id              = string
    enabled         = bool
    prefix          = string
    expiration_days = number
    transitions = list(object({
      days          = number
      storage_class = string
    }))
  }))
  default = []
}
