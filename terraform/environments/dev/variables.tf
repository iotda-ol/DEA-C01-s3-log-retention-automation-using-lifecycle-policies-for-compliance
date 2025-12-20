variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "retention_days" {
  description = "Number of days to retain logs"
  type        = number
  default     = 365
}

variable "bucket_prefix" {
  description = "Prefix for bucket names"
  type        = string
  default     = "logs"
}

variable "enable_ia_transition" {
  description = "Enable transition to STANDARD_IA"
  type        = bool
  default     = true
}

variable "ia_transition_days" {
  description = "Days before IA transition"
  type        = number
  default     = 30
}

variable "enable_glacier_transition" {
  description = "Enable transition to GLACIER"
  type        = bool
  default     = true
}

variable "glacier_transition_days" {
  description = "Days before Glacier transition"
  type        = number
  default     = 90
}

variable "enable_deep_archive" {
  description = "Enable transition to DEEP_ARCHIVE"
  type        = bool
  default     = false
}

variable "enable_versioning" {
  description = "Enable bucket versioning"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Enable server-side encryption"
  type        = bool
  default     = true
}

variable "encryption_algorithm" {
  description = "Encryption algorithm"
  type        = string
  default     = "AES256"
}

variable "enable_mfa_delete" {
  description = "Enable MFA delete"
  type        = bool
  default     = false
}

variable "enable_logging" {
  description = "Enable access logging"
  type        = bool
  default     = true
}

variable "enable_cloudwatch_alarm" {
  description = "Enable CloudWatch alarms"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}
