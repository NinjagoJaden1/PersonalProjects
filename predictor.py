import csv
import math
import argparse
from collections import defaultdict

# Extra emphasis for the home team
HOME_WEIGHT = 1.1  # multiplier applied to the home team's rating
HOME_ADVANTAGE = 3  # points added to predicted home score


def load_games(path):
    """Load games from a CSV path."""
    games = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('home_points') and row.get('away_points'):
                try:
                    games.append({
                        'date': row['date'],
                        'home_team': row['home_team'],
                        'away_team': row['away_team'],
                        'home_points': int(row['home_points']),
                        'away_points': int(row['away_points']),
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
    ratings = {team: vals['diff_sum'] / vals['games'] for team, vals in totals.items()}
    return ratings


def compute_team_point_avgs(games):
    """Return average points scored and allowed for each team."""
    totals = defaultdict(lambda: {'scored': 0, 'allowed': 0, 'games': 0})
    for g in games:
        totals[g['home_team']]['scored'] += g['home_points']
        totals[g['home_team']]['allowed'] += g['away_points']
        totals[g['home_team']]['games'] += 1

        totals[g['away_team']]['scored'] += g['away_points']
        totals[g['away_team']]['allowed'] += g['home_points']
        totals[g['away_team']]['games'] += 1

    avgs = {}
    for team, vals in totals.items():
        games_played = vals['games']
        avgs[team] = {
            'scored': vals['scored'] / games_played,
            'allowed': vals['allowed'] / games_played,
        }
    return avgs


def predict_final_score(home_team, away_team, avgs, home_advantage=HOME_ADVANTAGE):
    """Predict final score using team offensive and defensive averages."""
    h = avgs.get(home_team, {'scored': 0, 'allowed': 0})
    a = avgs.get(away_team, {'scored': 0, 'allowed': 0})
    home_score = (h['scored'] + a['allowed']) / 2 + home_advantage
    away_score = (a['scored'] + h['allowed']) / 2
    return round(home_score), round(away_score)


def predict_with_reasoning(home_team, away_team, ratings, k=0.1, home_weight=HOME_WEIGHT):
    """Return win probability plus explanation of the calculation."""
    raw_home = ratings.get(home_team, 0)
    rating_home = raw_home * home_weight
    rating_away = ratings.get(away_team, 0)
    diff = rating_home - rating_away
    prob_home = 1 / (1 + math.exp(-k * diff))
    reasoning = (
        f"Home rating {raw_home:.2f} x{home_weight:.2f}, "
        f"Away rating {rating_away:.2f}, diff {diff:.2f} -> prob {prob_home:.3f}"
    )
    return prob_home, reasoning


def main():
    parser = argparse.ArgumentParser(description="NBA Betting Predictor")
    parser.add_argument('--data', default='data/sample_games.csv', help='Path to games CSV data')
    parser.add_argument('home_team', help='Home team name')
    parser.add_argument('away_team', help='Away team name')
    args = parser.parse_args()

    games = load_games(args.data)
    ratings = compute_team_ratings(games)
    avgs = compute_team_point_avgs(games)

    prob, reason = predict_with_reasoning(args.home_team, args.away_team, ratings)
    home_score, away_score = predict_final_score(args.home_team, args.away_team, avgs)

    print(reason)
    print(f"Predicted probability {args.home_team} beats {args.away_team}: {prob:.3f}")
    print(f"Predicted final score: {args.home_team} {home_score} - {args.away_team} {away_score}")


if __name__ == '__main__':
    main()
