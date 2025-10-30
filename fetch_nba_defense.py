import requests
import pandas as pd
import time

url = "https://stats.nba.com/stats/leaguedashteamstats"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Referer": "https://www.nba.com/",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.nba.com"
}

params = {
    "College": "",
    "Conference": "",
    "Country": "",
    "DateFrom": "",
    "DateTo": "",
    "Division": "",
    "DraftPick": "",
    "DraftYear": "",
    "GameScope": "",
    "GameSegment": "",
    "Height": "",
    "LastNGames": "0",
    "LeagueID": "00",
    "Location": "",
    "MeasureType": "Defense",
    "Month": "0",
    "OpponentTeamID": "0",
    "Outcome": "",
    "PORound": "0",
    "PaceAdjust": "N",
    "PerMode": "PerGame",
    "Period": "0",
    "PlayerExperience": "",
    "PlayerPosition": "",
    "PlusMinus": "N",
    "Rank": "Y",
    "Season": "2025-26",
    "SeasonSegment": "",
    "SeasonType": "Regular Season",
    "ShotClockRange": "",
    "StarterBench": "",
    "TeamID": "0",
    "TwoWay": "0",
    "VsConference": "",
    "VsDivision": "",
    "Weight": ""
}

print("🔁 Fetching NBA Defense Data...")

for attempt in range(5):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200 and response.text.strip() != "":
            data = response.json()
            break
        print(f"⚠️ Attempt {attempt+1}/5 failed, retrying...")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Request failed: {e}")
        time.sleep(3)

# Process data
results = data["resultSets"][0]
headers = results["headers"]
rows = results["rowSet"]

df = pd.DataFrame(rows, columns=headers)
df.to_csv("nba_defense.csv", index=False)

print("✅ Defense data saved to nba_defense.csv")
