output "log_bucket_name" {
  description = "Name of the log storage bucket"
  value       = module.log_bucket.bucket_id
}

output "log_bucket_arn" {
  description = "ARN of the log storage bucket"
  value       = module.log_bucket.bucket_arn
}

output "access_logs_bucket_name" {
  description = "Name of the access logs bucket"
  value       = var.enable_logging ? module.access_logs_bucket[0].bucket_id : null
}

output "iam_role_arn" {
  description = "ARN of the S3 access IAM role"
  value       = module.s3_access_role.role_arn
}
