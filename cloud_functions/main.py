import requests
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import storage, bigquery
import os

def ingest_weather(request):
    try:
        yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        #yesterday = "2025-07-01"    # For testing purposes, set a fixed date

        print(f"Yesterday = {yesterday}")

        # Call API
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": 41.8781,
            "longitude": -87.6298,
            "start_date": yesterday,
            "end_date": yesterday,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "America/Chicago"
        }

        print("Calling Open-Meteo API...")
        r = requests.get(url, params=params)
        data = r.json()
        print("API response:", data)

        df = pd.DataFrame(data.get("daily", []))
        print("DataFrame head:", df.head())

        if df.empty:
            return "No data received from Open-Meteo API.", 500

        # Force float types
        float_cols = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
        for col in float_cols:
            if col in df.columns:
                df[col] = df[col].astype(float)

        # Save parquet locally
        file_name = f"weather_{yesterday}.parquet"
        local_path = f"/tmp/{file_name}"
        df.to_parquet(local_path, index=False)
        print(f"Parquet saved to {local_path}")

        # Upload to GCS
        bucket_name = os.environ.get("GCS_BUCKET")
        if not bucket_name:
            return "Missing GCS_BUCKET env var", 500

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(f"weather/{file_name}")
        blob.upload_from_filename(local_path)
        print(f"Uploaded to GCS at gs://{bucket_name}/weather/{file_name}")

        # Load to BigQuery
        bq_client = bigquery.Client()
        table_id = os.environ.get("BQ_TABLE")
        if not table_id:
            return "Missing BQ_TABLE env var", 500

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition="WRITE_APPEND",
        )

        uri = f"gs://{bucket_name}/weather/{file_name}"
        load_job = bq_client.load_table_from_uri(
            uri, table_id, job_config=job_config
        )
        load_job.result()
        print(f"Loaded to BigQuery table {table_id}")

        return f"Loaded weather data for {yesterday}", 200

    except Exception as e:
        print("ERROR:", str(e))
        return f"Error occurred: {str(e)}", 500
