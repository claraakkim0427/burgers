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

def fetch_places(location, radius, included_types, api_key):
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName.text,places.formattedAddress,places.types,places.websiteUri,places.internationalPhoneNumber,places.rating,places.googleMapsUri,places.businessStatus",
        "Content-Type": "application/json",
    }

    params = {
        "locationRestriction": {
            "circle": {
                "center": location,
                "radius": radius,
            }
        },
        "includedTypes": included_types,
        "maxResultCount": 20,
    }

    places_data = []
    has_next_page = True
    page_token = None

    while has_next_page:
        if page_token:
            params["pageToken"] = page_token

        response = requests.post(url, headers=headers, json=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
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
                    }
                )

        has_next_page = "nextPageToken" in data
        page_token = data.get("nextPageToken", None)

        if has_next_page:
            print(f"Fetching next page with token: {page_token}")
            time.sleep(2)  # Wait for 2 seconds before making the next request

    return places_data

# Fetch places data
api_key = os.environ["API_KEY"]
places_data = fetch_places(washington_dc, 5000, ["hamburger_restaurant"], api_key)

# Check the number of places fetched
print(f"Number of places fetched: {len(places_data)}")

# Convert to DataFrame and save to CSV
df = pd.DataFrame(places_data)
df.to_csv("output.csv", index=False)
print(df)

# Save raw JSON response to file
with open("output.json", "w") as f:
    json.dump(places_data, f, indent=4)