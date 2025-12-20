output "log_writer_role_arn" {
  description = "ARN of the log writer IAM role"
  value       = var.create_log_writer_role ? aws_iam_role.log_writer[0].arn : ""
}

output "log_writer_role_name" {
  description = "Name of the log writer IAM role"
  value       = var.create_log_writer_role ? aws_iam_role.log_writer[0].name : ""
}

output "log_reader_role_arn" {
  description = "ARN of the log reader IAM role"
  value       = var.create_log_reader_role ? aws_iam_role.log_reader[0].arn : ""
}

output "log_reader_role_name" {
  description = "Name of the log reader IAM role"
  value       = var.create_log_reader_role ? aws_iam_role.log_reader[0].name : ""
}

output "lifecycle_manager_role_arn" {
  description = "ARN of the lifecycle manager IAM role"
  value       = var.create_lifecycle_manager_role ? aws_iam_role.lifecycle_manager[0].arn : ""
}

output "lifecycle_manager_role_name" {
  description = "Name of the lifecycle manager IAM role"
  value       = var.create_lifecycle_manager_role ? aws_iam_role.lifecycle_manager[0].name : ""
}
