import requests
import pandas as pd
import time

def fetch_data(url, params, headers):
    for attempt in range(6):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=20)
            if r.status_code == 200 and r.text.strip() != "":
                return r.json()
            print(f"⚠️ Retry {attempt+1}/6 — status {r.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(4)
    return None


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Referer": "https://www.nba.com/",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.nba.com"
}

params = {
    "Season": "2025-26",
    "SeasonType": "Regular Season",
    "PerMode": "PerGame",
    "MeasureType": "Defense",
    "Rank": "Y",
    "PaceAdjust": "N",
}

print("🔁 Fetching NBA Defense Data (main endpoint)...")

main_url = "https://stats.nba.com/stats/leaguedashteamstats"
data = fetch_data(main_url, params, headers)

# fallback backup endpoint (NBA internal API — easier to scrape)
if data is None:
    print("⚠️ Main API failed — switching to backup endpoint...")
    backup_url = "https://cdn.nba.com/static/json/liveData/seasonTeamStats/seasonTeamStats_2025.json"
    data = fetch_data(backup_url, {}, headers)

if data is None:
    print("❌ Could not fetch NBA data — saving empty file to avoid workflow crash.")
    pd.DataFrame().to_csv("nba_defense.csv", index=False)
    exit(0)

print("✅ Data received — processing...")

# detect format (main API or backup)
if "resultSets" in data:
    results = data["resultSets"][0]
    headers = results["headers"]
    rows = results["rowSet"]
    df = pd.DataFrame(rows, columns=headers)
else:
    # backup JSON
    teams = data["teams"]
    df = pd.DataFrame(teams)

df.to_csv("nba_defense.csv", index=False)

print("✅ Defense data saved to nba_defense.csv")
