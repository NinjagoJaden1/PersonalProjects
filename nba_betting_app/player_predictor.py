import csv
import argparse
from collections import defaultdict


def load_player_stats(path):
    """Load player stats from CSV."""
    stats = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {
                'player': row['player'],
                'points': int(row['points']),
                'rebounds': int(row['rebounds']),
                'assists': int(row['assists']),
                'steals': int(row['steals']),
                'fgm': int(row['fgm']),
                'fga': int(row['fga']),
                'ftm': int(row['ftm']),
                'fta': int(row['fta'])
            }
            stats.append(entry)
    return stats


def compute_averages(stats):
    """Compute per-player averages."""
    totals = defaultdict(lambda: defaultdict(int))
    counts = defaultdict(int)
    for s in stats:
        p = s['player']
        counts[p] += 1
        for k, v in s.items():
            if k != 'player':
                totals[p][k] += v
    avgs = {}
    for player, sums in totals.items():
        games = counts[player]
        avgs[player] = {k: sums[k] / games for k in sums}
        # compute percentages
        fg_attempts = sums['fga']
        ft_attempts = sums['fta']
        avgs[player]['fg_pct'] = sums['fgm'] / fg_attempts if fg_attempts else 0
        avgs[player]['ft_pct'] = sums['ftm'] / ft_attempts if ft_attempts else 0
    return avgs


def predict_player(player, avgs):
    """Return the player's average stats as a simple prediction."""
    return avgs.get(player)


def main():
    parser = argparse.ArgumentParser(description="NBA Player Stats Predictor")

    parser.add_argument('--data', default='data/sample_player_stats.csv',
=======
    parser.add_argument('--data', default='nba_betting_app/data/sample_player_stats.csv',

                        help='Path to player stats CSV')
    parser.add_argument('player', help='Player name')
    args = parser.parse_args()

    stats = load_player_stats(args.data)
    avgs = compute_averages(stats)
    prediction = predict_player(args.player, avgs)

    if prediction is None:
        print(f"No data for player {args.player}")
        return

    print(f"Predicted stats for {args.player} (based on averages):")
    print(f"  Points: {prediction['points']:.1f}")
    print(f"  Rebounds: {prediction['rebounds']:.1f}")
    print(f"  Assists: {prediction['assists']:.1f}")
    print(f"  Steals: {prediction['steals']:.1f}")
    print(f"  FG%: {prediction['fg_pct']:.3f}")
    print(f"  FT%: {prediction['ft_pct']:.3f}")


if __name__ == '__main__':
    main()
