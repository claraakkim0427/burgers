import requests
import pandas as pd
import json
import os

# ny
bronx_ny = {"latitude": 40.8448, "longitude": -73.8648}
brooklyn_ny = {"latitude": 40.6782, "longitude": -73.9442}
manhattan_ny = {"latitude": 40.7831, "longitude": -73.9712}
queens_ny = {"latitude": 40.7282, "longitude": -73.7949}
staten_island_ny = {"latitude": 40.5795, "longitude": -74.1502}

# nj
newark_nj = {"latitude": 40.7357, "longitude": -74.1724}
jersey_city_nj = {"latitude": 40.7282, "longitude": -74.0776}
paterson_nj = {"latitude": 40.9168, "longitude": -74.1718}
elizabeth_nj = {"latitude": 40.6636, "longitude": -74.2107}
edison_nj = {"latitude": 40.5187, "longitude": -74.4121}

# ma
boston_ma = {"latitude": 42.3601, "longitude": -71.0589}
worcester_ma = {"latitude": 42.2626, "longitude": -71.8023}
springfield_ma = {"latitude": 42.1015, "longitude": -72.5898}
cambridge_ma = {"latitude": 42.3736, "longitude": -71.1097}

# pa
philadelphia_pa = {"latitude": 39.9526, "longitude": -75.1652}
pittsburgh_pa = {"latitude": 40.4406, "longitude": -79.9959}

# washington dc
washington_dc = {"latitude": 38.9072, "longitude": -77.0369}

response = requests.post(
    "https://places.googleapis.com/v1/places:searchNearby",
    headers={
        "X-Goog-Api-Key": os.environ["API_KEY"],
        "X-Goog-FieldMask": "places.displayName.text,places.formattedAddress,places.types,places.websiteUri,places.internationalPhoneNumber,places.rating,places.googleMapsUri,places.businessStatus",
        "Content-Type": "application/json",
    },
    json={
        "includedTypes": ["hamburger_restaurant"],
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": brooklyn_ny,
                "radius": 5000.0,
            }
        },
    },
)
data = response.json()

# Extract displayName text and other fields
places_data = []
for place in data.get("places", []):
    if place.get("businessStatus", "") == "OPERATIONAL":
        display_name = place.get("displayName", {}).get("text", "")
        formatted_address = place.get("formattedAddress", "")
        types = place.get("types", [])
        website_uri = place.get("websiteUri", "")
        international_phone_number = place.get("internationalPhoneNumber", "")
        rating = place.get("rating", "")
        google_maps_uri = place.get("googleMapsUri", "")

        places_data.append(
            {
                "displayName": display_name,
                "formattedAddress": formatted_address,
                "types": types,
                "websiteUri": website_uri,
                "internationalPhoneNumber": international_phone_number,
                "rating": rating,
                "googleMapsUri": google_maps_uri,
            })

# Convert to DataFrame and save to CSV
df = pd.DataFrame(places_data)
df.to_csv("output.csv", index=False)
print(df)

# Save raw JSON response to file
with open("output.json", "w") as f:
    json.dump(data, f, indent=4)
