variable "name_prefix" {
  description = "Prefix for IAM resource names"
  type        = string
}

variable "log_bucket_arn" {
  description = "ARN of the S3 log bucket"
  type        = string
}

variable "create_log_writer_role" {
  description = "Whether to create the log writer IAM role"
  type        = bool
  default     = true
}

variable "log_writer_assume_role_policy" {
  description = "Assume role policy for log writer role"
  type        = string
  default     = ""
}

variable "create_log_reader_role" {
  description = "Whether to create the log reader IAM role"
  type        = bool
  default     = true
}

variable "log_reader_assume_role_policy" {
  description = "Assume role policy for log reader role"
  type        = string
  default     = ""
}

variable "create_lifecycle_manager_role" {
  description = "Whether to create the lifecycle manager IAM role"
  type        = bool
  default     = true
}

variable "lifecycle_manager_assume_role_policy" {
  description = "Assume role policy for lifecycle manager role"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags to apply to IAM resources"
  type        = map(string)
  default     = {}
}
