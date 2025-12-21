variable "name_prefix" {
  description = "Prefix for IAM resource names"
  type        = string
}

variable "bucket_arn" {
  description = "ARN of the S3 bucket"
variable "project_name" {
  description = "Name of the project (used for resource naming)"
  type        = string
  default     = "s3-log-retention"
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
  description = "Tags to apply to IAM resources"
  type        = map(string)
  default     = {}
}

variable "create_lambda_role" {
  description = "Create IAM role for Lambda functions"
  type        = bool
  default     = true
}

variable "create_eventbridge_role" {
  description = "Create IAM role for EventBridge"
  type        = bool
  default     = false
}

variable "create_inventory_role" {
  description = "Create IAM role for S3 inventory"
  type        = bool
  default     = false
}

variable "create_cross_account_role" {
  description = "Create IAM role for cross-account access"
  type        = bool
  default     = false
}

variable "lambda_function_arn" {
  description = "ARN of Lambda function for EventBridge to invoke"
  type        = string
  default     = ""
}

variable "trusted_account_ids" {
  description = "List of AWS account IDs trusted for cross-account access"
  type        = list(string)
  default     = []
}

variable "require_mfa" {
  description = "Require MFA for cross-account access"
  type        = bool
  default     = true
}
