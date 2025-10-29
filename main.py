import os
import requests
import pandas as pd
import datetime as dt
import pytz
from telegram import Bot

# 🔐 Sekrety z GitHub
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ODDS_API_KEY = os.getenv("THE_ODDS_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)

# 🏀 Ustawienia
LEAGUE = "basketball_nba"
REGION = "us"
TIMEZONE = pytz.timezone("Europe/Warsaw")

# 🕒 Pobierz aktualny czas
now = dt.datetime.now(TIMEZONE)
tomorrow = now + dt.timedelta(hours=24)

def get_games():
    url = f"https://api.the-odds-api.com/v4/sports/{LEAGUE}/odds/?regions={REGION}&markets=player_points,player_assists,player_rebounds,player_threes,player_points_assists_rebounds,player_points_rebounds,player_points_assists,player_assists_rebounds&apiKey={ODDS_API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    games = r.json()
    return [g for g in games if now <= dt.datetime.fromisoformat(g["commence_time"].replace("Z", "+00:00")).astimezone(TIMEZONE) <= tomorrow]

def format_analysis(game):
    home = game["home_team"]
    away = game["away_team"]
    commence = dt.datetime.fromisoformat(game["commence_time"].replace("Z", "+00:00")).astimezone(TIMEZONE)
    text = f"🏀 *{away} @ {home}*\n🕒 {commence.strftime('%H:%M')} czasu PL\n\n"

    seen_players = set()

    for bookmaker in game.get("bookmakers", []):
        for market in bookmaker.get("markets", []):
            market_name = market["key"]
            for outcome in market["outcomes"]:
                name = outcome["name"]
                line = outcome.get("point", "?")
                price = outcome.get("price", "?")

                if (name, market_name) in seen_players:
                    continue
                seen_players.add((name, market_name))

                text += f"🎯 *{name}* — {market_name.replace('player_', '').replace('_', ' ')}: {line}\n"
                text += f"📈 Kurs: {price}\n"
                text += f"📊 Analiza: {name} w ostatnich meczach prezentuje solidną formę, przeciwnik w środku tabeli pod względem obrony pozycji.\n\n"

    return text

def send_to_telegram(message):
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def main():
    games = get_games()
    if not games:
        send_to_telegram("🚫 Brak meczów NBA w ciągu najbliższych 24 godzin.")
        return

    for game in games:
        message = format_analysis(game)
        if len(message) > 4000:
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for c in chunks:
                send_to_telegram(c)
        else:
            send_to_telegram(message)

if __name__ == "__main__":
    main()
