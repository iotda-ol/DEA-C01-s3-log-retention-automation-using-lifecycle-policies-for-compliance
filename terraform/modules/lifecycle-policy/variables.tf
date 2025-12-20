variable "bucket_id" {
  description = "ID of the S3 bucket to apply lifecycle policy"
  type        = string
}

variable "retention_days" {
  description = "Number of days to retain objects before deletion"
  type        = number
  default     = 365

  validation {
    condition     = var.retention_days > 0
    error_message = "Retention days must be greater than 0."
  }
}

variable "enable_ia_transition" {
  description = "Enable transition to STANDARD_IA storage class"
  type        = bool
  default     = false
}

variable "ia_transition_days" {
  description = "Number of days before transitioning to STANDARD_IA"
  type        = number
  default     = 30

  validation {
    condition     = var.ia_transition_days >= 30
    error_message = "IA transition must be at least 30 days."
  }
}

variable "enable_glacier_transition" {
  description = "Enable transition to GLACIER storage class"
  type        = bool
  default     = false
}

variable "glacier_transition_days" {
  description = "Number of days before transitioning to GLACIER"
  type        = number
  default     = 90

  validation {
    condition     = var.glacier_transition_days >= 1
    error_message = "Glacier transition days must be at least 1 day."
  }
}

variable "enable_deep_archive_transition" {
  description = "Enable transition to GLACIER_DEEP_ARCHIVE storage class"
  type        = bool
  default     = false
}

variable "deep_archive_transition_days" {
  description = "Number of days before transitioning to GLACIER_DEEP_ARCHIVE"
  type        = number
  default     = 180

  validation {
    condition     = var.deep_archive_transition_days >= 180
    error_message = "Deep Archive transition must be at least 180 days."
  }
}

variable "prefix" {
  description = "Object key prefix to filter lifecycle rule"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Object tags to filter lifecycle rule"
  type        = map(string)
  default     = {}
}

variable "cleanup_incomplete_uploads" {
  description = "Enable cleanup of incomplete multipart uploads"
  type        = bool
  default     = true
}

variable "incomplete_upload_days" {
  description = "Days before aborting incomplete multipart uploads"
  type        = number
  default     = 7

  validation {
    condition     = var.incomplete_upload_days > 0
    error_message = "Incomplete upload days must be greater than 0."
  }
}

variable "noncurrent_version_expiration_days" {
  description = "Days to retain noncurrent object versions"
  type        = number
  default     = 90
}

variable "enable_noncurrent_version_transitions" {
  description = "Enable transitions for noncurrent versions"
  type        = bool
  default     = false
}
