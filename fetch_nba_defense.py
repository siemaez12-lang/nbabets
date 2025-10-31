import requests
import time
import pandas as pd

URL = "https://stats.nba.com/stats/leaguedashteamstats"

HEADERS = {
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Accept-Language": "en-US,en;q=0.9",
}

PARAMS = {
    "MeasureType": "Defense",
    "PerMode": "PerGame",
    "Season": "2024-25",  # Możesz zmieniać
    "SeasonType": "Regular Season",
}

def fetch_data():
    for i in range(6):  # max 6 prób
        try:
            print(f"🔁 Fetching attempt {i+1}/6...")
            r = requests.get(URL, headers=HEADERS, params=PARAMS, timeout=15)
            if r.status_code == 200:
                data = r.json()["resultSets"][0]
                headers = data["headers"]
                rows = data["rowSet"]
                df = pd.DataFrame(rows, columns=headers)
                df.to_csv("nba_defense.csv", index=False)
                print("✅ Data saved to nba_defense.csv")
                return
            else:
                print(f"⚠️ Status {r.status_code}, retry in 3s...")
        except Exception as e:
            print(f"❌ Error: {e}, retry in 3s...")

        time.sleep(3)

    print("❌ Failed after 6 attempts")

if __name__ == "__main__":
    fetch_data()
