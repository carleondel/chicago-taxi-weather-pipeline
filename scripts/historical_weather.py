import requests
import pandas as pd

# Chicago coordinates
latitude = 41.8781
longitude = -87.6298

# Date range
start_date = "2023-06-01"
end_date = "2023-12-31"

# Daily variables
daily_vars = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum"
]

# URL
base_url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date,
    "end_date": end_date,
    "daily": ",".join(daily_vars),
    "timezone": "America/Chicago"
}

response = requests.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()
    
    # DataFrame construction
    daily = data["daily"]
    df = pd.DataFrame(daily)
    
    # save to Parquet
    df.to_parquet("historical_weather_2023.parquet", index=False)
    print("Parquet file saved: historical_weather_2023.parquet")
else:
    print("Download failed:", response.text)
