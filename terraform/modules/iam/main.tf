locals {
  # Build S3 actions based on permissions
  s3_actions = concat(
    var.enable_read ? [
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:ListBucket",
      "s3:GetBucketLocation",
    ] : [],
    var.enable_write ? [
      "s3:PutObject",
      "s3:PutObjectAcl",
    ] : [],
    var.enable_delete ? [
      "s3:DeleteObject",
      "s3:DeleteObjectVersion",
    ] : [],
    var.enable_lifecycle ? [
      "s3:GetLifecycleConfiguration",
      "s3:PutLifecycleConfiguration",
    ] : []
  )

  # Build object ARNs
  object_arns = [for arn in var.bucket_arns : "${arn}/*"]
}

# IAM Role
resource "aws_iam_role" "main" {
  name                 = var.role_name
  path                 = var.path
  max_session_duration = var.max_session_duration

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = var.services
        }
      }
    ]
  })

  tags = merge(
    {
      Name      = var.role_name
      ManagedBy = "Terraform"
    },
    var.tags
  )
}

# S3 Access Policy
resource "aws_iam_policy" "s3_access" {
  name        = "${var.role_name}-s3-policy"
  path        = var.path
  description = "S3 access policy for ${var.role_name}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "BucketLevelPermissions"
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetBucketLocation",
        ]
        Resource = var.bucket_arns
      },
      {
        Sid      = "ObjectLevelPermissions"
        Effect   = "Allow"
        Action   = local.s3_actions
        Resource = concat(var.bucket_arns, local.object_arns)
      }
    ]
  })

  tags = merge(
    {
      Name      = "${var.role_name}-s3-policy"
      ManagedBy = "Terraform"
    },
    var.tags
  )
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "s3_access" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.s3_access.arn
}
