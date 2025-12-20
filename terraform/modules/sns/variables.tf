variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "email" {
  description = "Email address for SNS notifications"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
