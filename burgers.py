import requests
import pandas as pd
import os

response = requests.post("https://places.googleapis.com/v1/places:searchNearby", 
    headers={"X-Goog-Api-Key": os.environ["API_KEY"]},
                         json={
  "includedTypes": ["restaurant"],
  "maxResultCount": 10,
  "locationRestriction": {
    "circle": {
      "center": {
        "latitude": 37.7937,
        "longitude": -122.3965},
      "radius": 500.0
    }
  }
})
data = response.json()
print(data)

