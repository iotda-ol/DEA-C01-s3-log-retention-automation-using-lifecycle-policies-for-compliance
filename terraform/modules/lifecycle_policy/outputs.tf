output "lifecycle_configuration_id" {
  description = "The ID of the lifecycle configuration"
  value       = aws_s3_bucket_lifecycle_configuration.log_retention_policy.id
}

output "retention_days" {
  description = "Configured retention period in days"
  value       = var.retention_days
}

output "rule_id" {
  description = "ID of the primary retention rule"
  value       = var.retention_rule_id
}
