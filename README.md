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

![Architecture Diagram](images/chicago-taxi-weather.png)


- **Terraform** for infrastructure-as-code.
- **Google Cloud Storage (GCS)** as the landing zone for raw weather data.
- **BigQuery** as the data warehouse for both taxi trips and weather data.
- **dbt** to transform data into staging and marts layers.
- **Cloud Functions** to orchestrate the daily ingestion pipeline.
- **Looker Studio** for data visualization.
- **GitHub Actions** for CI/CD.

## Project Structure

```
chicago-taxi-weather-pipeline/
│
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── terraform.tfvars
│   └── outputs.tf
│
├── cloud_functions/
│   ├── main.py
│   └── requirements.txt
│
├── scripts/
│   └── historical_weather.py
│
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── analyses/
│   ├── macros/
│   ├── seeds/
│   ├── snapshots/
│   ├── tests/
│   └── models/
│       ├── staging/
│       │   ├── stg_chicago_taxi_trips.sql
│       │   ├── stg_weather.sql
│       │   └── schema.yml
│       └── marts/
│           ├── mart_trips_weather.sql
│           └── schema.yml
│
├── .github/
│    └── workflows/
│         └── deploy.yml
└── README.md
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

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run historical weather download script

```
python scripts/historical_weather.py
```

This downloads historical weather data from Open-Meteo and saves it as a Parquet file locally.


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

---

## Cloud Function Deployment

The weather ingestion pipeline is implemented as a 2nd-gen Google Cloud Function. The function:

- Calls the Open-Meteo API
- Generates a Parquet file
- Uploads it to GCS
- Loads it into BigQuery (using WRITE_APPEND mode)

The function runs daily via Cloud Scheduler:

```bash
gcloud scheduler jobs create http weather-daily \
    --schedule="0 7 * * *" \
    --http-method=GET \
    --uri=https://us-central1-chicago-taxi-weather.cloudfunctions.net/ingest_weather \
    --time-zone="America/Chicago" \
    --location=us-central1
```

Note: The raw.weather table uses an append-only pattern. To avoid duplicate rows on repeated ingestion of the same date, a future enhancement could include deleting existing rows for the given date before loading new data.

---

## dbt

dbt is used to transform raw data into staging and marts layers. The mart is incremental:

- materialized as `incremental`
- using `date` as the unique key
- ensuring only new data is processed each run

### Initialize dbt profiles

Edit your `profiles.yml` to include your GCP project ID and service account JSON file path.

### Run dbt models

```bash
cd dbt
dbt run
```

### Run dbt tests

```bash
dbt test
```

## Looker Studio

Looker Studio connects directly to the BigQuery marts layer:

- Dataset: `chicago-taxi-weather.ctw_marts`
- Table: `mart_trips_weather`

Recommended visualizations:

- Average trip duration vs. temperature
- Average trip duration vs. precipitation
- Trends over time

---

## CI/CD

The pipeline includes GitHub Actions to:

- Validate Terraform syntax and plans.
- Run dbt build and tests.

---

## To-Do

- [ ] Complete Looker Studio dashboard.
- [ ] Implement column-level security for `payment_type`.
- [ ] Refactor CI/CD pipeline for deployments and tests.

---

## Column-Level Security

To restrict access to the `payment_type` column, implement BigQuery column-level access policies or use authorized views that exclude this column for non-authorized users.

---

# Future Automation

In the future, dbt can be automated using Cloud Run Jobs

1. Build a Docker image with dbt installed and the project code.
2. Deploy it as a Cloud Run Job.
3. Trigger the job daily via Cloud Scheduler.

This provides a lightweight and cost-effective solution for orchestrating dbt pipelines in production.

---

**Note:** Parquet files generated locally (e.g. `historical_weather_2023.parquet`) are ignored from version control and must be uploaded to GCS for BigQuery ingestion.