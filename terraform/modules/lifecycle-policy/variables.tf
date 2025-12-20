variable "bucket_id" {
  description = "The ID of the S3 bucket to apply lifecycle policies to"
  type        = string
}

variable "lifecycle_rules" {
  description = "List of lifecycle rules to apply to the bucket"
  type = list(object({
    id          = string
    enabled     = bool
    prefix      = optional(string)
    tags        = optional(map(string))
    transitions = optional(list(object({
      days          = number
      storage_class = string
    })))
    expiration_days = optional(number)
    noncurrent_transitions = optional(list(object({
      days          = number
      storage_class = string
    })))
    noncurrent_expiration_days = optional(number)
    abort_incomplete_days      = optional(number)
  }))
  default = []
}
