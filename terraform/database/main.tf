terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "0.76.0"
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

resource "yandex_mdb_postgresql_cluster" "db" {
  name = var.db_name
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
      max_connections = 395
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
    name = var.db_name
    owner = var.db_user
  }

  user {
    name = var.db_user
    password = var.db_password
    conn_limit = 50
    permission {
      database_name = var.db_name
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

output "db_host" {
  value = yandex_mdb_postgresql_cluster.db.host.0.fqdn
}