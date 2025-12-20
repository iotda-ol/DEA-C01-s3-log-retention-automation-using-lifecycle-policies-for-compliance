/**
 * Monitoring Module
 * CloudWatch metrics, alarms, and dashboards for S3 log retention
 */

data "aws_caller_identity" "current" {}

# CloudWatch metric alarm for bucket size
resource "aws_cloudwatch_metric_alarm" "bucket_size_alarm" {
  count = var.enable_size_alarm ? 1 : 0

  alarm_name          = "${var.bucket_name}-size-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = var.size_alarm_evaluation_periods
  metric_name         = "BucketSizeBytes"
  namespace           = "AWS/S3"
  period              = var.size_alarm_period
  statistic           = "Average"
  threshold           = var.size_alarm_threshold_bytes
  alarm_description   = "Alert when S3 bucket size exceeds threshold"
  alarm_actions       = var.alarm_actions

  dimensions = {
    BucketName  = var.bucket_name
    StorageType = "StandardStorage"
  }

  tags = var.tags
}

# CloudWatch metric alarm for number of objects
resource "aws_cloudwatch_metric_alarm" "object_count_alarm" {
  count = var.enable_object_count_alarm ? 1 : 0

  alarm_name          = "${var.bucket_name}-object-count-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = var.object_count_evaluation_periods
  metric_name         = "NumberOfObjects"
  namespace           = "AWS/S3"
  period              = var.object_count_period
  statistic           = "Average"
  threshold           = var.object_count_threshold
  alarm_description   = "Alert when number of objects exceeds threshold"
  alarm_actions       = var.alarm_actions

  dimensions = {
    BucketName  = var.bucket_name
    StorageType = "AllStorageTypes"
  }

  tags = var.tags
}

# CloudWatch metric alarm for 4xx errors
resource "aws_cloudwatch_metric_alarm" "error_4xx_alarm" {
  count = var.enable_error_alarms ? 1 : 0

  alarm_name          = "${var.bucket_name}-4xx-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "4xxErrors"
  namespace           = "AWS/S3"
  period              = 300
  statistic           = "Sum"
  threshold           = var.error_4xx_threshold
  alarm_description   = "Alert on high rate of 4xx errors"
  alarm_actions       = var.alarm_actions

  dimensions = {
    BucketName = var.bucket_name
  }

  tags = var.tags
}

# CloudWatch metric alarm for 5xx errors
resource "aws_cloudwatch_metric_alarm" "error_5xx_alarm" {
  count = var.enable_error_alarms ? 1 : 0

  alarm_name          = "${var.bucket_name}-5xx-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "5xxErrors"
  namespace           = "AWS/S3"
  period              = 300
  statistic           = "Sum"
  threshold           = var.error_5xx_threshold
  alarm_description   = "Alert on high rate of 5xx errors"
  alarm_actions       = var.alarm_actions

  dimensions = {
    BucketName = var.bucket_name
  }

  tags = var.tags
}

# CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "s3_monitoring" {
  count = var.create_dashboard ? 1 : 0

  dashboard_name = "${var.bucket_name}-monitoring"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/S3", "BucketSizeBytes", { stat = "Average", label = "Bucket Size" }]
          ]
          period = 86400
          stat   = "Average"
          region = data.aws_caller_identity.current.id
          title  = "Bucket Size Over Time"
        }
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/S3", "NumberOfObjects", { stat = "Average", label = "Object Count" }]
          ]
          period = 86400
          stat   = "Average"
          region = data.aws_caller_identity.current.id
          title  = "Number of Objects"
        }
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/S3", "AllRequests", { stat = "Sum", label = "All Requests" }],
            [".", "GetRequests", { stat = "Sum", label = "GET Requests" }],
            [".", "PutRequests", { stat = "Sum", label = "PUT Requests" }]
          ]
          period = 300
          stat   = "Sum"
          region = data.aws_caller_identity.current.id
          title  = "API Request Metrics"
        }
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/S3", "4xxErrors", { stat = "Sum", label = "4xx Errors" }],
            [".", "5xxErrors", { stat = "Sum", label = "5xx Errors" }]
          ]
          period = 300
          stat   = "Sum"
          region = data.aws_caller_identity.current.id
          title  = "Error Metrics"
        }
      }
    ]
  })
}

# SNS Topic for alarms (optional)
resource "aws_sns_topic" "alarm_topic" {
  count = var.create_sns_topic ? 1 : 0

  name              = "${var.bucket_name}-alarms"
  display_name      = "S3 Log Retention Alarms"
  kms_master_key_id = var.sns_kms_key_id

  tags = var.tags
}

# SNS Topic Subscription
resource "aws_sns_topic_subscription" "alarm_subscription" {
  count = var.create_sns_topic && length(var.alarm_email_endpoints) > 0 ? length(var.alarm_email_endpoints) : 0

  topic_arn = aws_sns_topic.alarm_topic[0].arn
  protocol  = "email"
  endpoint  = var.alarm_email_endpoints[count.index]
}

# CloudWatch Log Group for custom metrics
resource "aws_cloudwatch_log_group" "custom_metrics" {
  count = var.create_log_group ? 1 : 0

  name              = "/aws/s3/${var.bucket_name}/custom-metrics"
  retention_in_days = var.log_retention_days
  kms_key_id        = var.cloudwatch_kms_key_id

  tags = var.tags
}
