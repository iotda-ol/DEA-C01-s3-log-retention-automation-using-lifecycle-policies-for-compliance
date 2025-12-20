variable "role_name" {
  description = "Name of the IAM role"
  type        = string
}

variable "services" {
  description = "AWS services that can assume this role"
  type        = list(string)
  default     = ["ec2.amazonaws.com"]
}

variable "bucket_arns" {
  description = "ARNs of S3 buckets to grant access"
  type        = list(string)
}

variable "enable_read" {
  description = "Enable read access to S3 buckets"
  type        = bool
  default     = true
}

variable "enable_write" {
  description = "Enable write access to S3 buckets"
  type        = bool
  default     = false
}

variable "enable_delete" {
  description = "Enable delete access to S3 buckets"
  type        = bool
  default     = false
}

variable "enable_lifecycle" {
  description = "Enable lifecycle policy management"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags for IAM resources"
  type        = map(string)
  default     = {}
}

variable "path" {
  description = "Path for IAM role"
  type        = string
  default     = "/"
}

variable "max_session_duration" {
  description = "Maximum session duration in seconds"
  type        = number
  default     = 3600

  validation {
    condition     = var.max_session_duration >= 3600 && var.max_session_duration <= 43200
    error_message = "Session duration must be between 3600 and 43200 seconds."
  }
}
