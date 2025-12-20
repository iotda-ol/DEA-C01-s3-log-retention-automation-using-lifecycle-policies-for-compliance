variable "bucket_name" {
  description = "Name of the S3 bucket for log storage"
  type        = string
}

variable "force_destroy" {
  description = "Allow bucket to be destroyed even if it contains objects"
  type        = bool
  default     = false
}

variable "enable_versioning" {
  description = "Enable versioning for the S3 bucket"
  type        = bool
  default     = true
}

variable "kms_key_id" {
  description = "KMS key ID for bucket encryption (optional, defaults to AES256)"
  type        = string
  default     = ""
}

variable "access_log_bucket" {
  description = "S3 bucket for storing access logs (optional)"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Additional tags for the S3 bucket"
  type        = map(string)
  default     = {}
}
