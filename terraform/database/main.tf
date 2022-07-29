terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = ">= 0.77.0"
    }
    doppler = {
      source = "DopplerHQ/doppler"
      version = ">= 1.0.0"
    }
  }

  backend "s3" {
    endpoint = "storage.yandexcloud.net"
    bucket = "septa-portal"
    key = "terraform/database.tfstate"

    skip_region_validation = true
    skip_credentials_validation = true
  }
}

provider "doppler" {
  doppler_token = var.doppler_token_portal_prod
}

locals {
  db_name = "portal"
  db_user = "septa"
}

data "yandex_client_config" "config" {}

data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    endpoint = "storage.yandexcloud.net"
    bucket = "portal"
    key = "terraform/network.tfstate"

    skip_region_validation = true
    skip_credentials_validation = true
  }
}

resource "random_password" "db_password" {
  length = 32
  special = false
}

resource "yandex_mdb_postgresql_cluster" "db" {
  name = local.db_name
  environment = "PRESTABLE"
  network_id = data.terraform_remote_state.network.outputs.network_id

  config {
    version = 12
    resources {
      resource_preset_id = "b1.nano"
      disk_type_id = "network-ssd"
      disk_size = 16
    }
    postgresql_config = {
      max_connections = 100
      enable_parallel_hash = true
      vacuum_cleanup_index_scale_factor = 0.2
      autovacuum_vacuum_scale_factor = 0.34
      default_transaction_isolation = "TRANSACTION_ISOLATION_READ_COMMITTED"
      shared_preload_libraries = "SHARED_PRELOAD_LIBRARIES_AUTO_EXPLAIN,SHARED_PRELOAD_LIBRARIES_PG_HINT_PLAN"
    }
  }

  maintenance_window {
    type = "WEEKLY"
    day = "SAT"
    hour = 12
  }

  database {
    name = local.db_name
    owner = local.db_user
  }

  user {
    name = local.db_user
    password = random_password.db_password.result
    conn_limit = 50
    permission {
      database_name = local.db_name
    }
    settings = {
      default_transaction_isolation = "read committed"
      log_min_duration_statement = 5000
    }
  }

  host {
    zone = data.yandex_client_config.config.zone
    subnet_id = data.terraform_remote_state.network.outputs.subnet_id
  }
}

# Save the random password to Doppler
resource "doppler_secret" "db_password" {
  project = "portal"
  config = "prd"
  name = "DB_PASSWORD"
  value = random_password.db_password.result
}

# Save FQDN of the database
resource "doppler_secret" "db_host" {
  project = "portal"
  config = "prd"
  name = "DB_HOST"
  value = yandex_mdb_postgresql_cluster.db.host.0.fqdn
}