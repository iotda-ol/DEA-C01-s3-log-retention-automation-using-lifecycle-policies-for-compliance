# CloudWatch Monitoring Module

resource "aws_cloudwatch_dashboard" "log_retention" {
  dashboard_name = "${var.name_prefix}-log-retention"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/S3", "BucketSizeBytes", { stat = "Average" }],
            [".", "NumberOfObjects", { stat = "Average" }]
          ]
          period = 86400
          stat   = "Average"
          region = data.aws_region.current.name
          title  = "S3 Bucket Metrics"
        }
      }
    ]
  })
}

resource "aws_cloudwatch_metric_alarm" "bucket_size" {
  count = var.sns_topic_arn != null ? 1 : 0

  alarm_name          = "${var.name_prefix}-bucket-size-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "BucketSizeBytes"
  namespace           = "AWS/S3"
  period              = 86400
  statistic           = "Average"
  threshold           = var.bucket_size_threshold
  alarm_description   = "Alert when bucket size exceeds threshold"
  alarm_actions       = [var.sns_topic_arn]

  dimensions = {
    BucketName = var.bucket_name
    StorageType = "StandardStorage"
  }
}

data "aws_region" "current" {}
