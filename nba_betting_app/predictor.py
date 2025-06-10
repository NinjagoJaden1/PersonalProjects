import csv
import math
import argparse
from collections import defaultdict


def load_games(path):
    games = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['home_points'] and row['away_points']:
                try:
                    games.append({
                        'date': row['date'],
                        'home_team': row['home_team'],
                        'away_team': row['away_team'],
                        'home_points': int(row['home_points']),
                        'away_points': int(row['away_points'])
                    })
                except ValueError:
                    print(f"⚠️ Skipping bad row: {row}")
    return games


def compute_team_ratings(games):
    """Compute average point differential for each team."""
    totals = defaultdict(lambda: {'diff_sum': 0, 'games': 0})
    for g in games:
        diff = g['home_points'] - g['away_points']
        totals[g['home_team']]['diff_sum'] += diff
        totals[g['home_team']]['games'] += 1
        totals[g['away_team']]['diff_sum'] -= diff
        totals[g['away_team']]['games'] += 1
    ratings = {}
    for team, vals in totals.items():
        ratings[team] = vals['diff_sum'] / vals['games']
    return ratings


def predict(home_team, away_team, ratings, k=0.1):
    """Predict home team win probability using logistic on rating diff."""
    rating_home = ratings.get(home_team, 0)
    rating_away = ratings.get(away_team, 0)
    diff = rating_home - rating_away
    prob_home_win = 1 / (1 + math.exp(-k * diff))
    return prob_home_win


def main():
    parser = argparse.ArgumentParser(description="NBA Betting Predictor")

    parser.add_argument('--data', default='data/sample_games.csv')


    parser.add_argument('--data', default='nba_betting_app/data/sample_games.csv',


                        help='Path to games CSV data')
    parser.add_argument('home_team', help='Home team name')
    parser.add_argument('away_team', help='Away team name')
    args = parser.parse_args()

    games = load_games(args.data)
    ratings = compute_team_ratings(games)
    prob = predict(args.home_team, args.away_team, ratings)

    print(f"Predicted probability {args.home_team} beats {args.away_team}: {prob:.3f}")


if __name__ == '__main__':
    main()
