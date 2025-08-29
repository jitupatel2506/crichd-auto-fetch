# ─────────────────────────────────────────────────────────────────────────────
# File: scripts/fetch_crichd_api.py
# Purpose: Fetch CricHD-style source JSON and write live_stream/auto_fetch_crichd_api.json
# Schedule: Run via GitHub Actions every 10 minutes (see workflow below)
# ─────────────────────────────────────────────────────────────────────────────


#!/usr/bin/env python3
import json
import os
import sys
import hashlib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import List, Dict, Any


# Defaults (can be overridden via env vars in GitHub Actions if needed)
SOURCE_URL = os.getenv(
"CRICHD_SOURCE_URL",
"https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/main/api.json",
)
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "crichd-auto-fetch/auto_fetch_crichd_api.json")
THUMBNAIL_URL = os.getenv(
"THUMBNAIL_URL",
"https://gitlab.com/ranginfotech89/ipl_data_api/-/raw/main/stream_categories/cricket_league_vectors/all_live_streaming.png",
)
PLATFORM = "CricHD"
LINK_TYPE = "app"
OWNER_INFO = "Stream provided by public source"
SUBTEXT = "Live Streaming Now" # If you want dynamic text, change this.


# Whether channelNumber should be stable (derived from source id/name) or truly random
STABLE_CHANNEL_NUMBERS = True # set to False for new random numbers on each run




def stable_channel_number(key: str) -> int:
    """Derive a stable 1..9999 number from a string key (looks random but is repeatable)."""
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()
    n = int(h[:8], 16) % 9999 + 1  # 1..9999
    return n




def fetch_source(url: str) -> Any:
req = Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
try:
with urlopen(req, timeout=30) as resp:
raw = resp.read()
return json.loads(raw)
except (URLError, HTTPError) as e:
raise RuntimeError(f"Network error while fetching {url}: {e}")
except json.JSONDecodeError as e:
raise RuntimeError(f"Invalid JSON at {url}: {e}")




def transform(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
out = []
used_numbers = set()


for item in items:
name = (item.get("name") or item.get("id") or "Unknown").strip()
link = (item.get("link") or "").strip()
if not link:
# Skip entries without a playable link
continue


# Prefer a stable key based on id/name/link
key = str(item.get("id") or name or link)
num = stable_channel_number(key) if STABLE_CHANNEL_NUMBERS else None


# Ensure uniqueness of channelNumber within this file
if num is None:
# true random path
import random


num = random.randint(1, 9999)
while num in used_numbers:
num = (num % 9999) + 1
used_numbers.add(num)


out.append(
{
"channelNumber": num, # integer; JSON won't keep leading zeros like 0001
"platform": PLATFORM,
"linkType": LINK_TYPE,
"channelName": name,
"subText": SUBTEXT,
"startTime": "",
"ownerInfo": OWNER_INFO,
"channelUrl": link,
"thumbnail": THUMBNAIL_URL,
raise SystemExit(1)
