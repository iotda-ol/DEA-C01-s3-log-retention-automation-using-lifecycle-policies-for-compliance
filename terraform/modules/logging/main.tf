/**
 * Logging Module
 * Sets up CloudWatch and CloudTrail logging for S3 bucket monitoring
 */

# CloudWatch Log Group for S3 events
resource "aws_cloudwatch_log_group" "s3_events" {
  count = var.enable_cloudwatch_logging ? 1 : 0
  
  name              = "/aws/s3/${var.bucket_name}"
  retention_in_days = var.cloudwatch_retention_days

  tags = var.tags
}

# CloudWatch Metric Alarm for lifecycle policy failures
resource "aws_cloudwatch_metric_alarm" "lifecycle_failures" {
  count = var.enable_lifecycle_monitoring ? 1 : 0
  
  alarm_name          = "${var.bucket_name}-lifecycle-failures"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "4xxErrors"
  namespace           = "AWS/S3"
  period              = "300"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "This metric monitors S3 lifecycle policy failures"
  alarm_actions       = var.alarm_actions

  dimensions = {
    BucketName = var.bucket_name
  }

  tags = var.tags
}

# CloudWatch Metric Alarm for storage quota
resource "aws_cloudwatch_metric_alarm" "storage_quota" {
  count = var.enable_storage_monitoring ? 1 : 0
  
  alarm_name          = "${var.bucket_name}-storage-quota"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "BucketSizeBytes"
  namespace           = "AWS/S3"
  period              = "86400"
  statistic           = "Average"
  threshold           = var.storage_quota_bytes
  alarm_description   = "This metric monitors S3 bucket storage usage"
  alarm_actions       = var.alarm_actions

  dimensions = {
    BucketName  = var.bucket_name
    StorageType = "StandardStorage"
  }

  tags = var.tags
}

# CloudTrail for S3 data events
resource "aws_cloudtrail" "s3_trail" {
  count = var.enable_cloudtrail ? 1 : 0
  
  name                          = "${var.bucket_name}-trail"
  s3_bucket_name                = var.cloudtrail_bucket_name
  s3_key_prefix                 = "cloudtrail/${var.bucket_name}/"
  include_global_service_events = false
  is_multi_region_trail         = var.cloudtrail_multi_region
  enable_logging                = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true

    data_resource {
      type   = "AWS::S3::Object"
      values = ["${var.bucket_arn}/"]
    }
  }

  tags = var.tags
}

# SNS Topic for alerts
resource "aws_sns_topic" "log_alerts" {
  count = var.create_sns_topic ? 1 : 0
  
  name = "${var.bucket_name}-alerts"

  tags = var.tags
}

# SNS Topic Subscription
resource "aws_sns_topic_subscription" "log_alerts_email" {
  count = var.create_sns_topic && var.alert_email != "" ? 1 : 0
  
  topic_arn = aws_sns_topic.log_alerts[0].arn
  protocol  = "email"
  endpoint  = var.alert_email
}
