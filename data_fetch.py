import requests
import pandas as pd
from datetime import datetime

def fetch_earthquakes(start_time: datetime, end_time: datetime):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start_time.isoformat(),
        "endtime": end_time.isoformat(),
        "minmagnitude": 2.5
    }
    resp = requests.get(url, params=params)
    data = resp.json().get("features", [])
    records = []
    for feat in data:
        props = feat["properties"]
        coords = feat["geometry"]["coordinates"]
        records.append({
            "time": datetime.utcfromtimestamp(props["time"] / 1000),
            "place": props["place"],
            "mag": props["mag"],
            "lon": coords[0],
            "lat": coords[1],
            "depth": coords[2]
        })
    return pd.DataFrame(records)

def fetch_volcanoes():
    url = "https://raw.githubusercontent.com/matheus-devhub/Volcano-Dataset/main/volcano.csv"
    return pd.read_csv(url)
