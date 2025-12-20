output "role_arn" {
  description = "ARN of the IAM role"
  value       = aws_iam_role.s3_log_access.arn
}

output "role_name" {
  description = "Name of the IAM role"
  value       = aws_iam_role.s3_log_access.name
}

output "readonly_policy_arn" {
  description = "ARN of the readonly policy"
  value       = aws_iam_policy.readonly_log_access.arn
}
