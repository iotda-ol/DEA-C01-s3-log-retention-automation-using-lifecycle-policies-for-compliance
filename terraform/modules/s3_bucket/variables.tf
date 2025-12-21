variable "bucket_name" {
  description = "Name of the S3 bucket for log storage"
  type        = string
}

variable "tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}

variable "enable_versioning" {
  description = "Enable versioning for the S3 bucket"
  type        = bool
  default     = true
}

variable "encryption_type" {
  description = "Type of server-side encryption (AES256 or aws:kms)"
  type        = string
  default     = "AES256"
  validation {
    condition     = contains(["AES256", "aws:kms"], var.encryption_type)
    error_message = "Encryption type must be either AES256 or aws:kms"
  }
}

variable "kms_key_id" {
  description = "KMS key ID for encryption (required if encryption_type is aws:kms)"
  type        = string
  default     = ""
}

variable "enable_access_logging" {
  description = "Enable access logging for the bucket"
  type        = bool
  default     = false
}

variable "access_log_bucket" {
  description = "S3 bucket for storing access logs"
  type        = string
  default     = ""
}

variable "access_log_prefix" {
  description = "Prefix for access log objects"
  type        = string
  default     = "access-logs/"
}

variable "enable_inventory" {
  description = "Enable S3 inventory for the bucket"
  type        = bool
  default     = false
}

variable "inventory_frequency" {
  description = "Frequency of inventory reports (Daily or Weekly)"
  type        = string
  default     = "Weekly"
  validation {
    condition     = contains(["Daily", "Weekly"], var.inventory_frequency)
    error_message = "Inventory frequency must be either Daily or Weekly"
  }
}

variable "inventory_format" {
  description = "Format of inventory report (CSV, ORC, or Parquet)"
  type        = string
  default     = "CSV"
  validation {
    condition     = contains(["CSV", "ORC", "Parquet"], var.inventory_format)
    error_message = "Inventory format must be CSV, ORC, or Parquet"
  }
}

variable "inventory_destination_bucket" {
  description = "ARN of destination bucket for inventory reports (defaults to same bucket)"
  type        = string
  default     = ""
}

variable "inventory_prefix" {
  description = "Prefix for inventory report objects"
  type        = string
  default     = "inventory/"
}
