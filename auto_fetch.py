import requests
import json
import time
import random

# Constants
SOURCE_URL = "https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/main/api.json"
OUTPUT_FILE = "auto_fetch_crichd_api.json"
PLATFORM = "CricHD"
LINK_TYPE = "app"
SUB_TEXT = "Live Streaming Now"
OWNER_INFO = "Stream provided by public source"
THUMBNAIL = "https://gitlab.com/ranginfotech89/ipl_data_api/-/raw/main/stream_categories/cricket_league_vectors/all_live_streaming.png"

def fetch_and_transform():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        data = response.json()

        transformed_data = []
        for item in data:
            channel_number = random.randint(1, 9999)  # Random number for channelNumber
            transformed_item = {
                "channelNumber": channel_number,
                "platform": PLATFORM,
                "linkType": LINK_TYPE,
                "channelName": item.get("name", ""),
                "subText": SUB_TEXT,
                "startTime": "",
                "ownerInfo": OWNER_INFO,
                "channelUrl": item.get("link", ""),
                "thumbnail": THUMBNAIL
            }
            transformed_data.append(transformed_item)

        # Write to output JSON file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(transformed_data, f, indent=4)

        print(f"Data fetched and saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    while True:
        fetch_and_transform()
        # Sleep for 10 minutes (600 seconds)
        time.sleep(600)

if __name__ == "__main__":
    main()
