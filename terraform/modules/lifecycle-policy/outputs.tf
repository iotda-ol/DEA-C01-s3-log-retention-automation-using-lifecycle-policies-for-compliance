output "lifecycle_rule_ids" {
  description = "List of lifecycle rule IDs"
  value       = aws_s3_bucket_lifecycle_configuration.main.rule[*].id
}
