output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = var.enable_cloudwatch_logging ? aws_cloudwatch_log_group.s3_events[0].name : ""
}

output "cloudwatch_log_group_arn" {
  description = "ARN of the CloudWatch log group"
  value       = var.enable_cloudwatch_logging ? aws_cloudwatch_log_group.s3_events[0].arn : ""
}

output "cloudtrail_arn" {
  description = "ARN of the CloudTrail"
  value       = var.enable_cloudtrail ? aws_cloudtrail.s3_trail[0].arn : ""
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for alerts"
  value       = var.create_sns_topic ? aws_sns_topic.log_alerts[0].arn : ""
}

output "lifecycle_alarm_arn" {
  description = "ARN of the lifecycle monitoring alarm"
  value       = var.enable_lifecycle_monitoring ? aws_cloudwatch_metric_alarm.lifecycle_failures[0].arn : ""
}

output "storage_alarm_arn" {
  description = "ARN of the storage monitoring alarm"
  value       = var.enable_storage_monitoring ? aws_cloudwatch_metric_alarm.storage_quota[0].arn : ""
}
