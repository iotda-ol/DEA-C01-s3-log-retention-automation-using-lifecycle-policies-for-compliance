variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "prefix" {
  description = "Object key prefix for lifecycle rule"
  type        = string
  default     = ""
}

variable "retention_days" {
  description = "Number of days to retain logs before deletion"
  type        = number
  default     = 365
}

variable "transitions" {
  description = "List of storage class transitions"
  type = list(object({
    days          = number
    storage_class = string
  }))
  default = []
}

variable "enable_noncurrent_version_expiration" {
  description = "Enable expiration of noncurrent versions"
  type        = bool
  default     = true
}

variable "noncurrent_version_retention_days" {
  description = "Days to retain noncurrent versions"
  type        = number
  default     = 90
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
