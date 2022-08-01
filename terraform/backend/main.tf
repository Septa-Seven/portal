terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = ">= 0.77.0"
    }
  }

  backend "s3" {
    endpoint = "storage.yandexcloud.net"
    bucket = "septa-portal"
    key = "terraform/backend.tfstate"

    skip_region_validation = true
    skip_credentials_validation = true
  }
}

data "yandex_client_config" "config" {}

data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    endpoint = "storage.yandexcloud.net"
    bucket = "septa-portal"
    key = "terraform/network.tfstate"

    skip_region_validation = true
    skip_credentials_validation = true
  }
}

data "yandex_compute_image" "container-optimized-image" {
  family = "container-optimized-image"
}

resource "yandex_compute_instance" "instance-based-on-coi" {
  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.container-optimized-image.id
    }
  }
  network_interface {
    subnet_id = data.terraform_remote_state.network.outputs.subnet_id
    nat = true
    nat_ip_address = data.terraform_remote_state.network.outputs.portal_address
  }
  resources {
    cores = 2
    memory = 2
    core_fraction = 5
  }
  allow_stopping_for_update = true
  metadata = {
    docker-compose = templatefile("${path.module}/docker-compose.yaml.tftpl", {
      image_tag = var.image_tag,
      doppler_token = var.doppler_token_portal_prod
    })
    user-data = file("${path.module}/cloud_config.yaml")
  }
  service_account_id = var.service_account_id
}