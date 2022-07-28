terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = ">= 0.72.0"
    }
  }

  backend "s3" {
    endpoint = "storage.yandexcloud.net"
    bucket = "septa-portal"
    key = "terraform/network.tfstate"

    skip_region_validation = true
    skip_credentials_validation = true
  }
}

data "yandex_client_config" "config" {}

resource "yandex_vpc_network" "network" {
  name = "septa"
  description = "Septa cup network"
}

resource "yandex_vpc_subnet" "subnet" {
  name = "septa-${data.yandex_client_config.config.zone}"
  zone = data.yandex_client_config.config.zone
  network_id = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.5.0.0/24"]
}

resource "yandex_vpc_address" "web_address" {
  name = "web_address"

  external_ipv4_address {
    zone_id = data.yandex_client_config.config.zone
  }
}

output "network_id" {
  value = yandex_vpc_network.network.id
}

output "subnet_id" {
  value = yandex_vpc_subnet.subnet.id
}