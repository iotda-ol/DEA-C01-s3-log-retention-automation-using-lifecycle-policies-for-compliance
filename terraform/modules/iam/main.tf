# IAM Module for S3 Log Access

data "aws_caller_identity" "current" {}

resource "aws_iam_role" "s3_log_access" {
  name = "${var.name_prefix}-s3-log-access"
/**
 * IAM Module
 * Creates IAM roles and policies for S3 log retention automation
 */

# Data source for current AWS account
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

# IAM role for Lambda function (if using automated processing)
resource "aws_iam_role" "log_processor_role" {
  count = var.create_lambda_role ? 1 : 0

  name        = "${var.project_name}-log-processor-role"
  description = "IAM role for log processing Lambda functions"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "s3_log_access" {
  name = "${var.name_prefix}-s3-log-access-policy"
  role = aws_iam_role.s3_log_access.id
# Policy for S3 access
resource "aws_iam_role_policy" "s3_access_policy" {
  count = var.create_lambda_role ? 1 : 0

  name = "${var.project_name}-s3-access"
  role = aws_iam_role.log_processor_role[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ]
        Resource = [
          var.bucket_arn,
          "${var.bucket_arn}/*"
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${var.bucket_name}",
          "arn:aws:s3:::${var.bucket_name}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetBucketLifecycleConfiguration",
          "s3:PutBucketLifecycleConfiguration"
        ]
        Resource = var.bucket_arn
      }
    ]
  })
}

resource "aws_iam_policy" "readonly_log_access" {
  name        = "${var.name_prefix}-readonly-log-access"
  description = "Read-only access to log bucket"
          "s3:GetBucketLocation",
          "s3:GetLifecycleConfiguration",
          "s3:PutLifecycleConfiguration"
        ]
        Resource = "arn:aws:s3:::${var.bucket_name}"
      }
    ]
  })
}

# Attach AWS managed policy for Lambda basic execution
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  count = var.create_lambda_role ? 1 : 0

  role       = aws_iam_role.log_processor_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# IAM role for CloudWatch Events (EventBridge)
resource "aws_iam_role" "eventbridge_role" {
  count = var.create_eventbridge_role ? 1 : 0

  name        = "${var.project_name}-eventbridge-role"
  description = "IAM role for EventBridge to invoke Lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# Policy for EventBridge to invoke Lambda
resource "aws_iam_role_policy" "eventbridge_invoke_lambda" {
  count = var.create_eventbridge_role ? 1 : 0

  name = "${var.project_name}-invoke-lambda"
  role = aws_iam_role.eventbridge_role[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = var.lambda_function_arn != "" ? var.lambda_function_arn : "*"
      }
    ]
  })
}

# Service role for S3 inventory
resource "aws_iam_role" "s3_inventory_role" {
  count = var.create_inventory_role ? 1 : 0

  name        = "${var.project_name}-s3-inventory-role"
  description = "IAM role for S3 inventory"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# Cross-account access role (if needed)
resource "aws_iam_role" "cross_account_role" {
  count = var.create_cross_account_role ? 1 : 0

  name        = "${var.project_name}-cross-account-role"
  description = "IAM role for cross-account S3 access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = var.trusted_account_ids
        }
        Condition = var.require_mfa ? {
          Bool = {
            "aws:MultiFactorAuthPresent" = "true"
          }
        } : {}
      }
    ]
  })

  tags = var.tags
}

# Cross-account S3 access policy
resource "aws_iam_role_policy" "cross_account_s3_policy" {
  count = var.create_cross_account_role ? 1 : 0

  name = "${var.project_name}-cross-account-s3"
  role = aws_iam_role.cross_account_role[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          var.bucket_arn,
          "${var.bucket_arn}/*"
        ]
      }
    ]
  })

  tags = var.tags
          "arn:aws:s3:::${var.bucket_name}",
          "arn:aws:s3:::${var.bucket_name}/*"
        ]
      }
    ]
  })
}
