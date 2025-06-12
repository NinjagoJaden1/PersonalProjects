import os
from datetime import date
import requests
import pandas as pd
from tqdm import tqdm

DATA_DIR = "data"
GAMES_PATH = os.path.join(DATA_DIR, "sample_games.csv")
STATS_PATH = os.path.join(DATA_DIR, "sample_player_stats.csv")
API_KEY = "9df1a841-76f7-4aab-93f4-ef92a6b0abc1"
HEADERS = {"Authorization": API_KEY}
GAMES_URL = "https://api.balldontlie.io/v1/games"
STATS_URL = "https://api.balldontlie.io/v1/stats"


# === Helper ===
def _current_season_start() -> int:
    """Return the starting year of the most recent NBA season."""
    today = date.today()
    return today.year if today.month >= 10 else today.year - 1


# === Fetch Latest Games ===
def fetch_all_games(start_date: str, end_date: str) -> list:
    """Return all completed regular season games between the dates."""
    print(f"📅 Fetching games from {start_date} to {end_date}...")
    games = []
    cursor = None

    while True:
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "per_page": 100,
            "postseason": "false",
        }
        if cursor:
            params["cursor"] = cursor

        resp = requests.get(GAMES_URL, headers=HEADERS, params=params)
        if resp.status_code != 200:
            print(f"❌ Error {resp.status_code}: {resp.text}")
            break

        data = resp.json()
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
            if g["home_team_score"] is not None
            and g["visitor_team_score"] is not None
        ]

        games.extend(page_games)
        print(f"📦 Retrieved {len(page_games)} games... Total: {len(games)}")

        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            break

    print(f"✅ Total games fetched: {len(games)}")
    return games






# === Fetch Player Stats for a Single Game ===
def fetch_stats_for_game(game_id: int) -> list:
    """Fetch all player stats for a single game using cursor pagination."""
    stats = []
    cursor = None
    while True:
        params = {"game_ids[]": game_id, "per_page": 100}
        if cursor:
            params["cursor"] = cursor

        resp = requests.get(STATS_URL, params=params, headers=HEADERS)
        resp.raise_for_status()
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
                print(f"⚠️ No stats found for game {game['id']} ({game['date']})")
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


# === Main Entry Point ===
def main():
    season_start = _current_season_start()
    start_date = f"{season_start}-10-01"
    end_date = f"{season_start + 1}-06-30"

    games = fetch_all_games(start_date=start_date, end_date=end_date)
    stats = collect_player_stats(games)
    save_to_csv(GAMES_PATH, games)
    save_to_csv(STATS_PATH, stats)


if __name__ == "__main__":
    main()
