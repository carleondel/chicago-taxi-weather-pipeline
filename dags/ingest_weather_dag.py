from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import os

# DAG definition
default_args = {
    'owner': 'carleondel',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 2),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'ingest_weather_daily',
    default_args=default_args,
    schedule_interval='0 7 * * *', # every day at 7 AM UTC
    catchup=False,
)

# Task 1 - download weather data
download_weather = BashOperator(
    task_id='download_weather',
    bash_command='python /home/airflow/gcs/data/scripts/download_daily_weather.py',
    dag=dag,
)

# define yesterday date string for dynamic file naming
yesterday_ds = '{{ macros.ds_add(ds, -1) }}'
parquet_filename = f'weather_{yesterday_ds}.parquet'

# Task 2 - upload to GCS
upload_gcs = LocalFilesystemToGCSOperator(
    task_id='upload_parquet_to_gcs',
    src=f'/home/airflow/gcs/data/weather_{yesterday_ds}.parquet',
    dst=f'weather/{parquet_filename}',
    bucket='chicago-taxi-weather-weather-raw',
    dag=dag,
)

# Task 3 - load into BigQuery
load_bq = BigQueryInsertJobOperator(
    task_id='load_weather_to_bq',
    configuration={
        "load": {
            "sourceUris": [f"gs://chicago-taxi-weather-weather-raw/weather/{parquet_filename}"],
            "destinationTable": {
                "projectId": "chicago-taxi-weather",
                "datasetId": "raw",
                "tableId": "weather",
            },
            "sourceFormat": "PARQUET",
            "writeDisposition": "WRITE_TRUNCATE",
        }
    },
    dag=dag,
)

# Task 4 - run dbt
run_dbt = BashOperator(
    task_id='run_dbt',
    bash_command='cd /home/airflow/gcs/data/dbt/dbt && dbt run',
    dag=dag,
)

download_weather >> upload_gcs >> load_bq >> run_dbt
