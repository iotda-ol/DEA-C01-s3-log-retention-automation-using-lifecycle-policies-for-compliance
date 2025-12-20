output "log_bucket_id" {
  description = "ID of the log bucket"
  value       = module.log_bucket.bucket_id
}

output "log_bucket_arn" {
  description = "ARN of the log bucket"
  value       = module.log_bucket.bucket_arn
}

output "log_bucket_region" {
  description = "Region of the log bucket"
  value       = module.log_bucket.bucket_region
}

output "log_writer_role_arn" {
  description = "ARN of the log writer role"
  value       = module.iam.log_writer_role_arn
}

output "log_reader_role_arn" {
  description = "ARN of the log reader role"
  value       = module.iam.log_reader_role_arn
}

output "lifecycle_manager_role_arn" {
  description = "ARN of the lifecycle manager role"
  value       = module.iam.lifecycle_manager_role_arn
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = module.logging.cloudwatch_log_group_name
}

output "sns_topic_arn" {
  description = "ARN of the SNS alert topic"
  value       = module.logging.sns_topic_arn
}

output "kms_key_id" {
  description = "ID of the KMS encryption key"
  value       = var.enable_kms_encryption ? aws_kms_key.log_encryption[0].id : ""
}

output "kms_key_arn" {
  description = "ARN of the KMS encryption key"
  value       = var.enable_kms_encryption ? aws_kms_key.log_encryption[0].arn : ""
}
