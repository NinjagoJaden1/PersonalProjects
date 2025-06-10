"""Download a full season of NBA games and player box scores."""

import os
import requests
import pandas as pd
from tqdm import tqdm

DATA_DIR = "data"
GAMES_PATH = os.path.join(DATA_DIR, "sample_games.csv")
STATS_PATH = os.path.join(DATA_DIR, "sample_player_stats.csv")
GAMES_URL = "https://www.balldontlie.io/api/v1/games"
STATS_URL = "https://www.balldontlie.io/api/v1/stats"


def fetch_season_games(season: int = 2023) -> list:
    """Fetch all completed games for a season."""
    params = {"seasons[]": season, "per_page": 100, "page": 1}
    games = []
    page = 1
    total_pages = 1
    with tqdm(desc="games", unit="page") as bar:
        while page <= total_pages:
            params["page"] = page
            resp = requests.get(GAMES_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            total_pages = data["meta"]["total_pages"]
            for g in data.get("data", []):
                if g["home_team_score"] == 0 or g["visitor_team_score"] == 0:
                    continue
                games.append({
                    "id": g["id"],
                    "date": g["date"][:10],
                    "home_team": g["home_team"]["full_name"],
                    "away_team": g["visitor_team"]["full_name"],
                    "home_points": g["home_team_score"],
                    "away_points": g["visitor_team_score"],
                })
            page += 1
            bar.update(1)
    return games


def fetch_stats_for_game(game_id: int):
    """Fetch all player stats for a single game."""
    params = {"game_ids[]": game_id, "per_page": 100, "page": 1}
    page = 1
    total_pages = 1
    stats = []
    while page <= total_pages:
        params["page"] = page
        resp = requests.get(STATS_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        total_pages = data["meta"]["total_pages"]
        stats.extend(data["data"])
        page += 1
    return stats


def collect_player_stats(games):
    """Collect player stats for a list of game dicts."""
    all_stats = []
    for game in tqdm(games, desc="player stats", unit="game"):
        for stat in fetch_stats_for_game(game["id"]):
            team = stat["team"]["full_name"]
            opponent = game["away_team"] if team == game["home_team"] else game["home_team"]
            all_stats.append({
                "game_id": game["id"],
                "date": game["date"],
                "player_id": stat["player"]["id"],
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
    return all_stats


def save_to_csv(path: str, rows: list):
    os.makedirs(DATA_DIR, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"✅ Saved {len(rows)} rows to {path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Download NBA data for a season")
    parser.add_argument("--season", type=int, default=2023, help="Season start year, e.g. 2023 for 2023-24")
    args = parser.parse_args()

    games = fetch_season_games(args.season)
    stats = collect_player_stats(games)
    save_to_csv(GAMES_PATH, games)
    save_to_csv(STATS_PATH, stats)


if __name__ == "__main__":
    main()
