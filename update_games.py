import os
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
from tqdm import tqdm

DATA_DIR = "data"
GAMES_PATH = os.path.join(DATA_DIR, "recent_games.csv")
STATS_PATH = os.path.join(DATA_DIR, "recent_player_stats.csv")
API_KEY = "9df1a841-76f7-4aab-93f4-ef92a6b0abc1"
HEADERS = {"Authorization": API_KEY}
GAMES_URL = "https://api.balldontlie.io/v1/games"
STATS_URL = "https://api.balldontlie.io/v1/stats"

# === Fetch Games in Backward Chunks ===
def fetch_recent_games(limit: int = 500) -> list:
    games = []
    end = datetime.today()  # ⬅️ Start fetching games FROM this date and go backward

    print(f"📅 Fetching the most recent {limit} games...")

    while len(games) < limit:
        chunk_start = end - relativedelta(months=3)  # ⬅️ 3-month fetch window
        s = chunk_start.strftime("%Y-%m-%d")
        e = end.strftime("%Y-%m-%d")
        print(f"🗓️  Chunk: {s} → {e}")

        cursor = None
        while True:
            params = {
                "start_date": s,
                "end_date": e,
                "per_page": 100,
            }
            if cursor:
                params["cursor"] = cursor

            resp = requests.get(GAMES_URL, headers=HEADERS, params=params)
            if resp.status_code != 200:
                print(f"❌ Error {resp.status_code}: {resp.text}")
                return games

            data = resp.json()
            if not data["data"]:
                print(f"⚠️ No games found between {s} and {e}.")
                break

            page_games = [
                {
                    "id": g["id"],
                    "date": g["date"][:10],
                    "home_team": g["home_team"]["full_name"],
                    "away_team": g["visitor_team"]["full_name"],
                    "home_points": g["home_team_score"],
                    "away_points": g["visitor_team_score"],
                }
                for g in data["data"]
                if g["home_team_score"] is not None and g["visitor_team_score"] is not None
            ]

            games.extend(page_games)
            print(f"📦 Retrieved {len(page_games)} games... Total so far: {len(games)}")

            if len(games) >= limit:
                print("✅ Reached game limit. Stopping.")
                return games[:limit]

            cursor = data.get("meta", {}).get("next_cursor")
            if not cursor:
                break

        end = chunk_start  # move window backward

    print(f"✅ Finished. Total games collected: {len(games)}")
    return games[:limit]


# === Fetch Player Stats for One Game ===
def fetch_stats_for_game(game_id: int) -> list:
    stats = []
    cursor = None
    while True:
        params = {"game_ids[]": game_id, "per_page": 100}
        if cursor:
            params["cursor"] = cursor

        for _ in range(5):
            resp = requests.get(STATS_URL, params=params, headers=HEADERS)
            if resp.status_code == 429:
                print(f"⏳ Rate limited fetching stats for game {game_id}. Sleeping 10s...")
                time.sleep(10)
                continue
            elif resp.status_code != 200:
                print(f"❌ Error fetching stats for game {game_id}: {resp.text}")
                return stats
            break

        time.sleep(1.2)
        data = resp.json()
        stats.extend(data.get("data", []))

        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            break
    return stats


# === Collect Stats for All Games ===
def collect_player_stats(games):
    all_stats = []
    for game in tqdm(games, desc="player stats", unit="game"):
        try:
            game_stats = fetch_stats_for_game(game["id"])
            if not game_stats:
                print(f"⚠️ No stats for game {game['id']} ({game['date']})")
                continue
            for stat in game_stats:
                team = stat["team"]["full_name"]
                opponent = (
                    game["away_team"] if team == game["home_team"] else game["home_team"]
                )
                all_stats.append({
                    "game_id": game["id"],
                    "date": game["date"],
                    "player": stat["player"]["full_name"],
                    "team": team,
                    "opponent": opponent,
                    "points": stat["pts"],
                    "rebounds": stat["reb"],
                    "assists": stat["ast"],
                    "steals": stat["stl"],
                    "fgm": stat["fgm"],
                    "fga": stat["fga"],
                    "ftm": stat["ftm"],
                    "fta": stat["fta"],
                })
        except Exception as e:
            print(f"❌ Failed to fetch stats for game {game['id']}: {e}")
    return all_stats


# === Save to CSV ===
def save_to_csv(path: str, rows: list):
    os.makedirs(DATA_DIR, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"✅ Saved {len(rows)} rows to {path}")


# === Main ===
def main():
    games = fetch_recent_games(limit=500)

    if not games:
        print("⚠️ No games found.")
        return

    save_to_csv(GAMES_PATH, games)

    # Optional: Enable this if you want player stats too
    # stats = collect_player_stats(games)
    # save_to_csv(STATS_PATH, stats)


if __name__ == "__main__":
    main()
