# Chicago Taxi Weather Pipeline

This repository contains the solution to the Astrafy Data Engineer Challenge.

## Challenge Description

Astrafy is helping out the city of Chicago with some of its analytics. One of the many datasets of interest refers to the “Chicago Taxi trips” which is publicly available on BigQuery.

The mayor of Chicago assumes that the weather conditions affect the duration of the trips. Because of this, he wants us to build a small Looker Studio dashboard that shows the eventual insight that weather conditions affect trip duration.

### Requirements

- Filter the taxi trips data on `trip_start_timestamp` from 2023-06-01 to 2023-12-31.
- Ingest new weather data daily for the day before.
- All infrastructure must be hosted in Google Cloud.
- All resources must be created via Terraform.
- Use dbt for data transformations.
- OPTIONAL: only your email should have access to the column `payment_type`.

## Architecture Overview

- **Terraform** for infrastructure-as-code.
- **Google Cloud Storage (GCS)** as the landing zone for raw weather data.
- **BigQuery** as the data warehouse for both taxi trips and weather data.
- **dbt** to transform data into staging and marts layers.
- **Cloud Composer (Airflow)** to orchestrate the daily ingestion pipeline.
- **Looker Studio** for data visualization.

## Project Structure

```
chicago-taxi-weather-pipeline/
│
├── README.md
├── .gitignore
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│
├── dags/
│   ├── ingest_weather_dag.py
│
├── scripts/
│   ├── download_weather.py
│
├── dbt/
│   ├── chicago_taxi_weather/
│
├── .github/
│    ├── workflows/
│         ├── deploy.yml
```

## How to Run Locally

### 1. Clone the repository

```
git clone https://github.com/carleondel/chicago-taxi-weather-pipeline.git
cd chicago-taxi-weather-pipeline
```

### 2. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run Python script

```
python scripts/download_weather.py
```

This will download the weather data for the previous day and save it as a JSON file locally.

## Terraform

### Initialize Terraform

```
cd terraform
terraform init
```

### Plan

```
terraform plan -var-file="terraform.tfvars"
```

### Apply

```
terraform apply -var-file="terraform.tfvars"
```

## dbt

### Initialize dbt profiles

Edit your `profiles.yml` to include your GCP project ID and service account JSON file path.

### Run dbt models

```
cd dbt/chicago_taxi_weather
dbt run
```

## Airflow (Cloud Composer)

The Airflow DAG `ingest_weather_dag.py` performs the following tasks:

- Downloads daily weather data from the Open-Meteo API.
- Uploads raw data to GCS.
- Loads data into BigQuery.
- Runs dbt transformations.

## Looker Studio

Looker Studio will be connected to the BigQuery `marts` layer to visualize:

- Average trip duration vs. temperature.
- Average trip duration vs. precipitation.
- Trends over time.

## To-Do

- Create Terraform resources for BigQuery datasets and GCS buckets.
- Finalize dbt models for staging and marts layers.
- Integrate Airflow DAG with GCS and BigQuery.
- Build Looker Studio dashboard.
- Implement column-level security for `payment_type` if required.