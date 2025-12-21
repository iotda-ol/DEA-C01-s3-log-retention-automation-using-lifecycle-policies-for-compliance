output "lambda_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = var.create_lambda_role ? aws_iam_role.log_processor_role[0].arn : ""
}

output "lambda_role_name" {
  description = "Name of the Lambda execution role"
  value       = var.create_lambda_role ? aws_iam_role.log_processor_role[0].name : ""
}

output "eventbridge_role_arn" {
  description = "ARN of the EventBridge role"
  value       = var.create_eventbridge_role ? aws_iam_role.eventbridge_role[0].arn : ""
}

output "cross_account_role_arn" {
  description = "ARN of the cross-account access role"
  value       = var.create_cross_account_role ? aws_iam_role.cross_account_role[0].arn : ""
}

output "s3_inventory_role_arn" {
  description = "ARN of the S3 inventory role"
  value       = var.create_inventory_role ? aws_iam_role.s3_inventory_role[0].arn : ""
}
