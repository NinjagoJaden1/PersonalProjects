import argparse
from predictor import (
    load_games,
    compute_team_ratings,
    compute_team_point_avgs,

    compute_team_players,


    predict_with_reasoning,
    predict_final_score,
)
from player_predictor import load_player_stats, compute_averages, predict_player
from teams import ALL_TEAMS

DEFAULT_GAMES_PATH = 'data/sample_games.csv'
DEFAULT_STATS_PATH = 'data/sample_player_stats.csv'


def interactive_mode(games_path, stats_path):
    games = load_games(games_path)
    player_stats = load_player_stats(stats_path)
    team_players = compute_team_players(player_stats)

    teams = sorted(ALL_TEAMS)
    players = sorted({s['player'] for s in player_stats})

    print("Select an option:\n1) Predict game outcome\n2) Predict player stats")
    choice = input("Enter 1 or 2: ").strip()
    if choice == '1':
        print("Available teams: " + ", ".join(teams))
        home = input("Home team: ")
        away = input("Away team: ")

        ratings = compute_team_ratings(games, trade_date=None)
        avgs = compute_team_point_avgs(games, trade_date=None)

        ratings = compute_team_ratings(games)
        avgs = compute_team_point_avgs(games)

        prob, reason = predict_with_reasoning(home, away, ratings)
        home_score, away_score = predict_final_score(home, away, avgs)
        print(reason)
        print(f"Predicted probability {home} beats {away}: {prob:.3f}")
        print(f"Predicted final score: {home} {home_score} - {away} {away_score}")

        print(f"Players {home}: {', '.join(team_players.get(home, []))}")
        print(f"Players {away}: {', '.join(team_players.get(away, []))}")


    elif choice == '2':
        print("Available players: " + ", ".join(players))
        player = input("Player name: ")
        avgs = compute_averages(player_stats)
        stats = predict_player(player, avgs)
        if stats:
            print(f"Predicted stats for {player} (averages):")
            print(f"  Points: {stats['points']:.1f}")
            print(f"  Rebounds: {stats['rebounds']:.1f}")
            print(f"  Assists: {stats['assists']:.1f}")
            print(f"  Steals: {stats['steals']:.1f}")
            print(f"  FG%: {stats['fg_pct']:.3f}")
            print(f"  FT%: {stats['ft_pct']:.3f}")
        else:
            print(f"No data for player {player}")
    else:
        print("Invalid selection")


def main():
    parser = argparse.ArgumentParser(description="Interactive NBA betting helper")
    parser.add_argument('--games', default=DEFAULT_GAMES_PATH, help='Path to games CSV')
    parser.add_argument('--stats', default=DEFAULT_STATS_PATH, help='Path to player stats CSV')
    args = parser.parse_args()

    interactive_mode(args.games, args.stats)


if __name__ == '__main__':
    main()
