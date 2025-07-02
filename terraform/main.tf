terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "weather_raw" {
  name     = "${var.project_id}-weather-raw"
  location = var.region
}

resource "google_bigquery_dataset" "raw" {
  dataset_id = "raw"
  location   = var.region
}

resource "google_bigquery_dataset" "staging" {
  dataset_id = "staging"
  location   = var.region
}

resource "google_bigquery_dataset" "marts" {
  dataset_id = "marts"
  location   = var.region
}

#resource "google_composer_environment" "composer_env" {
#  name   = "composer-env"
#  region = var.region
#
#  config {
#    node_count = 3
#  }
#}


