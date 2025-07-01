import requests
import datetime
import json

def download_weather():
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    url = f"https://api.open-meteo.com/v1/forecast?latitude=41.88&longitude=-87.63&daily=temperature_2m_max,precipitation_sum&timezone=America%2FChicago&start_date={yesterday}&end_date={yesterday}"
    
    response = requests.get(url)
    data = response.json()

    file_path = f"weather_{yesterday}.json"
    with open(file_path, "w") as f:
        json.dump(data, f)

    print(f"Weather data saved to {file_path}")

if __name__ == "__main__":
    download_weather()