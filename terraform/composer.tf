resource "google_composer_environment" "composer_env" {
  name   = "composer-env"
  region = var.region

  config {
    node_config {
      service_account = "composer-service-account@chicago-taxi-weather.iam.gserviceaccount.com"
    }

    software_config {
      image_version = "composer-2.13.5-airflow-2.10.5"

      env_variables = {
        AIRFLOW_VAR_PROJECT_ID = var.project_id
      }

      pypi_packages = {
        "apache-airflow-providers-google" = ""
        "pandas" = ""
        "requests" = ""
      }
    }
  }
}
