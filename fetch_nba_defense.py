import requests
import pandas as pd

url = "https://cdn.nba.com/static/json/liveData/analytics/leagueDefenseStats.json"

print("🔁 Fetching NBA Defense Data...")

try:
    response = requests.get(url, timeout=10)
    data = response.json()
except Exception as e:
    print("❌ Request failed:", e)
    exit(1)

teams = data["leagueDefenseStats"]["teams"]

df = pd.DataFrame(teams)

df.to_csv("nba_defense_overall.csv", index=False)

print("✅ NBA defense data saved to nba_defense_overall.csv")
