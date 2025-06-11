"""Daily updater for NBA games and player stats from balldontlie.io."""

import csv
import os
import requests
from typing import List, Dict, Set, Tuple
from tqdm import tqdm

GAMES_URL = "https://www.balldontlie.io/api/v1/games"
STATS_URL = "https://www.balldontlie.io/api/v1/stats"
GAME_FILE = os.path.join("data", "nba_games.csv")
STAT_FILE = os.path.join("data", "player_stats.csv")


def fetch_all_games(season: int) -> List[Dict]:
    """Return all game objects for a season."""
    params = {"seasons[]": season, "per_page": 100, "page": 1}
    resp = requests.get(GAMES_URL, params=params)
    resp.raise_for_status()
    first = resp.json()
    total_pages = first["meta"]["total_pages"]
    games = first["data"]

    for page in tqdm(range(2, total_pages + 1), desc="Games", unit="page"):
        params["page"] = page
        resp = requests.get(GAMES_URL, params=params)
        resp.raise_for_status()
        games.extend(resp.json()["data"])
    return games


def fetch_stats_for_game(game_id: int) -> List[Dict]:
    """Return all player stats for a given game."""
    params = {"game_ids[]": game_id, "per_page": 100, "page": 1}
    resp = requests.get(STATS_URL, params=params)
    resp.raise_for_status()
    first = resp.json()
    total_pages = first["meta"]["total_pages"]
    stats = first["data"]

    for page in range(2, total_pages + 1):
        params["page"] = page
        resp = requests.get(STATS_URL, params=params)
        resp.raise_for_status()
        stats.extend(resp.json()["data"])
    return stats


def load_existing_ids(game_path: str, stat_path: str) -> Tuple[Set[int], Set[Tuple[int, int]]]:
    """Load existing game ids and (game_id, player_id) keys."""
    game_ids: Set[int] = set()
    stat_keys: Set[Tuple[int, int]] = set()

    if os.path.exists(game_path):
        with open(game_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("id"):
                    game_ids.add(int(row["id"]))
    if os.path.exists(stat_path):
        with open(stat_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (int(row["game_id"]), int(row.get("player_id", 0)))
                stat_keys.add(key)
    return game_ids, stat_keys


def append_rows(path: str, fieldnames: List[str], rows: List[Dict]):
    new_file = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if new_file:
            writer.writeheader()
        writer.writerows(rows)


def update_nba_data(season: int = 2023) -> None:
    """Fetch and append new NBA games and player stats."""
    try:
        game_ids, stat_keys = load_existing_ids(GAME_FILE, STAT_FILE)
        games = fetch_all_games(season)
    except Exception as exc:
        print(f"Error fetching games: {exc}")
        return

    new_game_rows = []
    new_stat_rows = []

    for game in tqdm(games, desc="Processing games", unit="game"):
        gid = game["id"]
        if gid in game_ids:
            continue
        new_game_rows.append({
            "id": gid,
            "date": game["date"][:10],
            "home_team": game["home_team"]["full_name"],
            "away_team": game["visitor_team"]["full_name"],
            "home_points": game["home_team_score"],
            "away_points": game["visitor_team_score"],
        })
        game_ids.add(gid)

        try:
            stats = fetch_stats_for_game(gid)
        except Exception as exc:
            print(f"Failed to fetch stats for game {gid}: {exc}")
            continue
        for s in stats:
            key = (gid, s["player"]["id"])
            if key in stat_keys:
                continue
            new_stat_rows.append({
                "game_id": gid,
                "player_id": s["player"]["id"],
                "player": s["player"]["full_name"],
                "team": s["team"]["full_name"],
                "points": s["pts"],
                "assists": s["ast"],
                "rebounds": s["reb"],
            })
            stat_keys.add(key)

    if new_game_rows:
        append_rows(GAME_FILE, ["id", "date", "home_team", "away_team", "home_points", "away_points"], new_game_rows)
        print(f"✅ {len(new_game_rows)} new games added")
    else:
        print("No new games found")

    if new_stat_rows:
        append_rows(STAT_FILE, ["game_id", "player_id", "player", "team", "points", "assists", "rebounds"], new_stat_rows)
        print(f"✅ {len(new_stat_rows)} new player stat lines added")
    else:
        print("No new player stats found")


def _schedule_loop():
    import schedule
    import time

    schedule.every().day.at("04:00").do(update_nba_data)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    _schedule_loop()
