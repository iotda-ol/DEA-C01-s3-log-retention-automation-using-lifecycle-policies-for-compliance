variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
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
  description = "Server-side encryption algorithm (AES256 or aws:kms)"
  type        = string
  default     = "AES256"

  validation {
    condition     = contains(["AES256", "aws:kms"], var.encryption_algorithm)
    error_message = "Encryption algorithm must be AES256 or aws:kms."
  }
}

variable "kms_key_id" {
  description = "KMS key ID for encryption (required if algorithm is aws:kms)"
  type        = string
  default     = null
}

variable "enable_logging" {
  description = "Enable server access logging"
  type        = bool
  default     = true
}

variable "logging_bucket" {
  description = "Target bucket for access logs"
  type        = string
  default     = null
}

variable "logging_prefix" {
  description = "Prefix for access log objects"
  type        = string
  default     = "access-logs/"
}

variable "block_public_access" {
  description = "Block all public access to the bucket"
  type        = bool
  default     = true
}

variable "force_destroy" {
  description = "Allow bucket deletion even if it contains objects"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Additional tags for the bucket"
  type        = map(string)
  default     = {}
}

variable "object_lock_enabled" {
  description = "Enable object lock for compliance"
  type        = bool
  default     = false
}

variable "mfa_delete" {
  description = "Enable MFA delete protection"
  type        = bool
  default     = false
}
