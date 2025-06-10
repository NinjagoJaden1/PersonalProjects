import requests
import pandas as pd
from tqdm import tqdm
import os

DATA_DIR = 'data'
OUTPUT_PATH = os.path.join(DATA_DIR, 'sample_games.csv')

def fetch_all_games(season=2023):
    games = []
    page = 1
    total_pages = 1  # placeholder

    print(f"Fetching NBA games from season {season}...")

    while page <= total_pages:
        url = f"https://www.balldontlie.io/api/v1/games?seasons[]={season}&per_page=100&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Failed on page {page}")
            break

        data = response.json()
        total_pages = data['meta']['total_pages']
        for game in data['data']:
            if game['home_team_score'] == 0 or game['visitor_team_score'] == 0:
                continue  # skip games not yet played

            games.append({
                'date': game['date'][:10],
                'home_team': game['home_team']['full_name'],
                'away_team': game['visitor_team']['full_name'],
                'home_points': game['home_team_score'],
                'away_points': game['visitor_team_score']
            })

        page += 1

    return games

def save_games_to_csv(games):
    os.makedirs(DATA_DIR, exist_ok=True)
    df = pd.DataFrame(games)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Saved {len(games)} games to {OUTPUT_PATH}")

def main():
    games = fetch_all_games()
    save_games_to_csv(games)

if __name__ == '__main__':
    main()
