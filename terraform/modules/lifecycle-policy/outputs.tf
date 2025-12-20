output "lifecycle_configuration_id" {
  description = "The ID of the lifecycle configuration"
  value       = aws_s3_bucket_lifecycle_configuration.log_lifecycle.id
}
