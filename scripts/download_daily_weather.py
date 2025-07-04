import requests
import pandas as pd
from datetime import datetime, timedelta

# calculate yesterday's date
yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

# API endpoint
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 41.8781,
    "longitude": -87.6298,
    "start_date": yesterday,
    "end_date": yesterday,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "America/Chicago"
}

r = requests.get(url, params=params)
data = r.json()

# transform into DataFrame
df = pd.DataFrame(data["daily"])

# save as Parquet file
path = f"/home/airflow/gcs/data/weather_{yesterday}.parquet"
df.to_parquet(path, index=False)
print(f"Saved {path}")
