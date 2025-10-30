#!/usr/bin/env python3
# fetch_nba_defense.py
"""
Fetch 'Teams - Defense Dash - Overall' stats from NBA Stats and save to CSV/JSON.
Designed to be run daily (GitHub Actions / cron).
"""

import requests
import time
import json
import pandas as pd
import os
from datetime import datetime

# Output files
OUT_CSV = "nba_defense_overall.csv"
OUT_JSON = "nba_defense_overall.json"

# NBA Stats endpoint for team defense dashboard (best-effort)
NBA_URL = "https://stats.nba.com/stats/teamdashboarddefense"

# Headers to mimic a real browser (helps avoid blocking)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/116.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Connection": "keep-alive",
}

# Params: Season is tuneable; set to current season or "2025-26" as needed
PARAMS = {
    "DateFrom": "",
    "DateTo": "",
    "DrillDown": "TEAM",
    "LeagueID": "00",
    "PerMode": "PerGame",        # or "Per100Possessions" / "Totals"
    "PlusMinus": "N",
    "Rank": "N",
    "Season": "2025-26",        # <- change if needed, you asked for 25/26 season data
    "SeasonSegment": "",
    "SeasonType": "Regular Season",
    "StarterBench": "",
    "TeamID": "",
    "VsConference": "",
    "VsDivision": "",
    "Outcome": "",
    "Location": "",
    "Month": "0",
    "OpponentTeamID": "0",
    "PORound": "0",
    "GameSegment": "",
    "DateTo": "",
    "GameScope": "",
}

MAX_RETRIES = 3
RETRY_DELAY = 3


def fetch_nba_stats():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(NBA_URL, headers=HEADERS, params=PARAMS, timeout=15)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"NBA Stats responded {resp.status_code}. Body preview: {resp.text[:200]}")
        except Exception as e:
            print("Request error:", e)
        if attempt < MAX_RETRIES:
            print(f"Retrying in {RETRY_DELAY} sec (attempt {attempt}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)
    return None


def parse_and_save(data):
    """
    Parse the NBA JSON response and save a CSV + JSON with readable columns.
    Structure of response: resultSets array with headers and rowSet.
    """
    if not data:
        print("No data to parse.")
        return False

    # Attempt to find the main resultSet (try common keys)
    result_sets = data.get("resultSets") or data.get("resultSet") or []
    if not result_sets:
        print("No resultSets in response.")
        return False

    # Take the first resultSet that looks like team rows
    chosen = None
    for rs in result_sets:
        headers = rs.get("headers", [])
        rows = rs.get("rowSet", [])
        # heuristic: must contain TEAM_ID or TEAM_NAME or TEAM_ABBREVIATION
        if any(h.lower().startswith("team") for h in headers) and rows:
            chosen = rs
            break
    if not chosen:
        # fallback: pick the first
        chosen = result_sets[0]

    headers = chosen.get("headers", [])
    rows = chosen.get("rowSet", [])

    df = pd.DataFrame(rows, columns=headers)

    # Save CSV and JSON with timestamp
    ts = datetime.utcnow().isoformat() + "Z"
    df["fetched_at_utc"] = ts

    df.to_csv(OUT_CSV, index=False)
    df.to_json(OUT_JSON, orient="records", force_ascii=False)

    print(f"Saved {len(df)} rows -> {OUT_CSV}, {OUT_JSON}")
    return True


def main():
    print("Fetching NBA Defense Dash Overall ... (Season param:", PARAMS.get("Season"), ")")
    data = fetch_nba_stats()
    ok = parse_and_save(data)
    if not ok:
        print("Failed to fetch or parse NBA stats.")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
