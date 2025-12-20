output "dashboard_arn" {
  description = "ARN of the CloudWatch dashboard"
  value       = var.create_dashboard ? aws_cloudwatch_dashboard.s3_monitoring[0].dashboard_arn : ""
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for alarms"
  value       = var.create_sns_topic ? aws_sns_topic.alarm_topic[0].arn : ""
}

output "log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = var.create_log_group ? aws_cloudwatch_log_group.custom_metrics[0].name : ""
}

output "size_alarm_arn" {
  description = "ARN of the bucket size alarm"
  value       = var.enable_size_alarm ? aws_cloudwatch_metric_alarm.bucket_size_alarm[0].arn : ""
}

output "object_count_alarm_arn" {
  description = "ARN of the object count alarm"
  value       = var.enable_object_count_alarm ? aws_cloudwatch_metric_alarm.object_count_alarm[0].arn : ""
}
