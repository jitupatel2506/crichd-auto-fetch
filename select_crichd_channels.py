#!/usr/bin/env python3
import json
import requests

# Source JSON URL
SOURCE_URL = "https://raw.githubusercontent.com/jitupatel2506/crichd-auto-fetch/refs/heads/main/crichd-auto-fetch/auto_fetch_crichd_api.json"

# Output file
OUTPUT_FILE = "crichd-auto-fetch/auto_crichd_selected_api.json"

# ✅ Array 1: channelName to select from source
SELECTED_CHANNELS = [
    "Willow HD 2",
    "Willow HD",
    "Sky Sports Cricket"
    #"TNT 4"
    #"Star Sports 1",
    #"Willow HD",
    #"LaLiGA"
    
]

# ✅ Array 2: replacement names (same order as above)
REPLACEMENT_NAMES = [
    "CPL 2025",
    "UAE TRI-SERIES",
    "SA_vs_ENG"
    #"SL Tour of ZIM 2025",
    #"SL Tour of ZIM 2025(Alternative)",
    #"100 FINAL",
    #"La - LiGA 2025-26"
]

def main():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        source_data = response.json()
    except Exception as e:
        print("❌ Error fetching source JSON:", e)
        return

    selected_data = []

    for i, original_name in enumerate(SELECTED_CHANNELS):
        replacement_name = REPLACEMENT_NAMES[i]

        for item in source_data:
            if item["channelName"] == original_name:
                new_item = item.copy()
                new_item["channelName"] = replacement_name
                selected_data.append(new_item)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(selected_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Selected JSON saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
