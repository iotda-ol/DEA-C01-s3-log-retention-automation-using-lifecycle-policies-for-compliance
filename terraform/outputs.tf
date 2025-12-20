output "log_bucket_id" {
  description = "ID of the log storage bucket"
  value       = module.s3_bucket.bucket_id
}

output "log_bucket_arn" {
  description = "ARN of the log storage bucket"
  value       = module.s3_bucket.bucket_arn
}

output "log_bucket_domain_name" {
  description = "Domain name of the log bucket"
  value       = module.s3_bucket.bucket_domain_name
}

output "lifecycle_policy_id" {
  description = "ID of the lifecycle policy"
  value       = module.lifecycle_policy.policy_id
}

output "iam_role_arn" {
  description = "ARN of the IAM role for S3 access"
  value       = module.iam.role_arn
}

output "monitoring_dashboard_name" {
  description = "Name of the CloudWatch dashboard"
  value       = var.enable_monitoring ? module.cloudwatch[0].dashboard_name : null
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for alerts"
  value       = var.enable_monitoring && var.alarm_email != "" ? module.sns[0].topic_arn : null
}
