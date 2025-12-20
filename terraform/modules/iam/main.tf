/**
 * IAM Module
 * Creates IAM roles and policies for S3 log management
 */

# IAM Role for Lambda functions or EC2 instances to write logs
resource "aws_iam_role" "log_writer" {
  count = var.create_log_writer_role ? 1 : 0
  
  name               = "${var.name_prefix}-log-writer"
  assume_role_policy = var.log_writer_assume_role_policy

  tags = var.tags
}

# Policy for writing logs to S3
resource "aws_iam_role_policy" "log_writer" {
  count = var.create_log_writer_role ? 1 : 0
  
  name = "${var.name_prefix}-log-writer-policy"
  role = aws_iam_role.log_writer[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ]
        Resource = "${var.log_bucket_arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = var.log_bucket_arn
      }
    ]
  })
}

# IAM Role for reading and validating logs
resource "aws_iam_role" "log_reader" {
  count = var.create_log_reader_role ? 1 : 0
  
  name               = "${var.name_prefix}-log-reader"
  assume_role_policy = var.log_reader_assume_role_policy

  tags = var.tags
}

# Policy for reading logs from S3
resource "aws_iam_role_policy" "log_reader" {
  count = var.create_log_reader_role ? 1 : 0
  
  name = "${var.name_prefix}-log-reader-policy"
  role = aws_iam_role.log_reader[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:ListBucket",
          "s3:ListBucketVersions"
        ]
        Resource = [
          var.log_bucket_arn,
          "${var.log_bucket_arn}/*"
        ]
      }
    ]
  })
}

# IAM Role for lifecycle management
resource "aws_iam_role" "lifecycle_manager" {
  count = var.create_lifecycle_manager_role ? 1 : 0
  
  name               = "${var.name_prefix}-lifecycle-manager"
  assume_role_policy = var.lifecycle_manager_assume_role_policy

  tags = var.tags
}

# Policy for managing lifecycle policies
resource "aws_iam_role_policy" "lifecycle_manager" {
  count = var.create_lifecycle_manager_role ? 1 : 0
  
  name = "${var.name_prefix}-lifecycle-manager-policy"
  role = aws_iam_role.lifecycle_manager[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetLifecycleConfiguration",
          "s3:PutLifecycleConfiguration",
          "s3:GetBucketVersioning",
          "s3:ListBucket"
        ]
        Resource = var.log_bucket_arn
      }
    ]
  })
}
