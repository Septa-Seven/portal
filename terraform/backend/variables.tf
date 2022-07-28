variable "image_tag" {
  type = string
}

variable "service_account_id" {
  type = string
}

variable "doppler_token_portal_prod" {
  type = string
  sensitive = true
}
