output "bucket_id" {
  description = "The ID (name) of the S3 bucket"
  value       = aws_s3_bucket.log_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.log_bucket.arn
}

output "bucket_domain_name" {
  description = "The domain name of the S3 bucket"
  value       = aws_s3_bucket.log_bucket.bucket_domain_name
}

output "bucket_regional_domain_name" {
  description = "The regional domain name of the S3 bucket"
  value       = aws_s3_bucket.log_bucket.bucket_regional_domain_name
}

output "log_writer_policy_arn" {
  description = "The ARN of the IAM policy for log writers"
  value       = aws_iam_policy.log_writer_policy.arn
}

output "log_writer_role_arn" {
  description = "The ARN of the IAM role for log writers"
  value       = aws_iam_role.log_writer_role.arn
}

output "log_writer_instance_profile_name" {
  description = "The name of the instance profile for EC2 instances"
  value       = aws_iam_instance_profile.log_writer_instance_profile.name
}

output "lifecycle_policy_details" {
  description = "Summary of lifecycle policy configuration"
  value = {
    retention_days             = var.retention_days
    transition_to_ia_days      = var.transition_to_ia_days
    transition_to_glacier_days = var.transition_to_glacier_days
    versioning_enabled         = var.enable_versioning
  }
}
