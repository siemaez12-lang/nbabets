import requests
import pandas as pd

# NBA API endpoint for defense dash
url = "https://stats.nba.com/stats/leaguedashteamstats"

params = {
    "MeasureType": "Defense",
    "PerMode": "PerGame",
    "Season": "2024-25",
    "SeasonType": "Regular Season"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nba.com"
}

print("🔁 Fetching NBA Defense Data...")

response = requests.get(url, params=params, headers=headers)

if response.status_code != 200:
    print("❌ NBA API request failed")
    print(response.text)
    exit(1)

data = response.json()

headers = data["resultSets"][0]["headers"]
rows = data["resultSets"][0]["rowSet"]

df = pd.DataFrame(rows, columns=headers)

df.to_csv("nba_defense_overall.csv", index=False)

print("✅ NBA defense data saved to nba_defense_overall.csv")
