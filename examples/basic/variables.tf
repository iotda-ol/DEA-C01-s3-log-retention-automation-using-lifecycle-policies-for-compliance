variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "s3-log-retention-basic"
}

variable "bucket_name" {
  description = "Name of the S3 bucket for log storage"
  type        = string
}

variable "retention_days" {
  description = "Number of days to retain logs (DEA-C01 compliance: 365 days)"
  type        = number
  default     = 365
}

variable "enable_versioning" {
  description = "Enable S3 versioning for the bucket"
  type        = bool
  default     = true
}

variable "encryption_type" {
  description = "Type of server-side encryption (AES256 or aws:kms)"
  type        = string
  default     = "AES256"
}

variable "create_lambda_role" {
  description = "Create IAM role for Lambda functions"
  type        = bool
  default     = false
}

variable "enable_monitoring" {
  description = "Enable CloudWatch monitoring and alarms"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "production"
    Project     = "S3LogRetention"
    ManagedBy   = "Terraform"
    Compliance  = "DEA-C01"
  }
}
