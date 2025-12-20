output "bucket_id" {
  description = "The name of the bucket"
  value       = aws_s3_bucket.log_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the bucket"
  value       = aws_s3_bucket.log_bucket.arn
}

output "bucket_region" {
  description = "The AWS region where the bucket resides"
  value       = aws_s3_bucket.log_bucket.region
}

output "bucket_domain_name" {
  description = "The bucket domain name"
  value       = aws_s3_bucket.log_bucket.bucket_domain_name
}
