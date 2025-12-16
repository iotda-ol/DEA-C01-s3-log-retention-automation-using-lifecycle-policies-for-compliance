variable "bucket_name" {
  description = "Name of the S3 bucket for log storage. Must be globally unique."
  type        = string
  default     = "server-logs-retention-bucket"
}

variable "retention_days" {
  description = "Number of days to retain logs before deletion (default: 365 days for 1 year compliance)"
  type        = number
  default     = 365
}

variable "transition_to_ia_days" {
  description = "Number of days before transitioning to Infrequent Access (IA) storage class for cost optimization"
  type        = number
  default     = 90
}

variable "transition_to_glacier_days" {
  description = "Number of days before transitioning to Glacier storage class for further cost optimization"
  type        = number
  default     = 180
}

variable "enable_versioning" {
  description = "Enable versioning for the S3 bucket"
  type        = bool
  default     = true
}

variable "kms_key_id" {
  description = "KMS key ID for S3 bucket encryption. If not provided, AES-256 encryption will be used."
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags to apply to all resources for compliance and cost tracking"
  type        = map(string)
  default = {
    Environment = "production"
    Purpose     = "log-retention"
    Compliance  = "1-year-retention"
    ManagedBy   = "terraform"
  }
}

variable "aws_region" {
  description = "AWS region for resource deployment"
  type        = string
  default     = "us-east-1"
}
