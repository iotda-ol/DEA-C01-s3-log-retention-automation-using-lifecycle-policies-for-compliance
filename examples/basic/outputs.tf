output "bucket_id" {
  description = "The ID of the S3 bucket"
  value       = module.log_bucket.bucket_id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = module.log_bucket.bucket_arn
}

output "bucket_region" {
  description = "The region of the S3 bucket"
  value       = module.log_bucket.bucket_region
}

output "lifecycle_configuration_id" {
  description = "ID of the lifecycle configuration"
  value       = module.lifecycle_policy.lifecycle_configuration_id
}

output "retention_days" {
  description = "Configured retention period in days"
  value       = module.lifecycle_policy.retention_days
}

output "lambda_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = module.iam.lambda_role_arn
}

output "dashboard_arn" {
  description = "ARN of the CloudWatch dashboard"
  value       = module.monitoring.dashboard_arn
}
