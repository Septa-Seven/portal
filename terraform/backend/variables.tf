variable "image_tag" {
  type = string
}

variable "service_account_id" {
  type = string
}

variable "environment" {
  type = string
  default = ""
  sensitive = true
}
