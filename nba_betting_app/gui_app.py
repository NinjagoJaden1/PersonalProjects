import tkinter as tk
from tkinter import ttk, messagebox
from predictor import load_games, compute_team_ratings, predict
from player_predictor import load_player_stats, compute_averages, predict_player

GAMES_PATH = 'data/sample_games.csv'
STATS_PATH = 'data/sample_player_stats.csv'


def load_data():
    games = load_games(GAMES_PATH)
    player_stats = load_player_stats(STATS_PATH)
    team_set = {g['home_team'] for g in games} | {g['away_team'] for g in games}
    player_set = {s['player'] for s in player_stats}
    ratings = compute_team_ratings(games)
    player_avgs = compute_averages(player_stats)
    return sorted(team_set), sorted(player_set), ratings, player_avgs


class BettingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('NBA Betting Helper')
        teams, players, ratings, player_avgs = load_data()
        self.ratings = ratings
        self.player_avgs = player_avgs

        self.notebook = ttk.Notebook(self)
        self.game_frame = ttk.Frame(self.notebook)
        self.player_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.game_frame, text='Game Prediction')
        self.notebook.add(self.player_frame, text='Player Stats')
        self.notebook.pack(expand=True, fill='both')

        # Game prediction UI
        ttk.Label(self.game_frame, text='Home Team:').grid(column=0, row=0, padx=5, pady=5)
        self.home_var = tk.StringVar(value=teams[0])
        ttk.Combobox(self.game_frame, textvariable=self.home_var, values=teams).grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(self.game_frame, text='Away Team:').grid(column=0, row=1, padx=5, pady=5)
        self.away_var = tk.StringVar(value=teams[1])
        ttk.Combobox(self.game_frame, textvariable=self.away_var, values=teams).grid(column=1, row=1, padx=5, pady=5)

        ttk.Button(self.game_frame, text='Predict', command=self.predict_game).grid(column=0, row=2, columnspan=2, pady=10)

        self.game_result = ttk.Label(self.game_frame, text='')
        self.game_result.grid(column=0, row=3, columnspan=2, pady=5)

        # Player stats UI
        ttk.Label(self.player_frame, text='Player:').grid(column=0, row=0, padx=5, pady=5)
        self.player_var = tk.StringVar(value=players[0])
        ttk.Combobox(self.player_frame, textvariable=self.player_var, values=players).grid(column=1, row=0, padx=5, pady=5)

        ttk.Button(self.player_frame, text='Show Stats', command=self.predict_player_stats).grid(column=0, row=1, columnspan=2, pady=10)

        self.stats_text = tk.Text(self.player_frame, width=40, height=6, state='disabled')
        self.stats_text.grid(column=0, row=2, columnspan=2, pady=5)

    def predict_game(self):
        home = self.home_var.get()
        away = self.away_var.get()
        if home == away:
            messagebox.showerror('Error', 'Teams must be different')
            return
        prob = predict(home, away, self.ratings)
        self.game_result.config(text=f'Probability {home} beats {away}: {prob:.3f}')

    def predict_player_stats(self):
        player = self.player_var.get()
        stats = predict_player(player, self.player_avgs)
        if not stats:
            messagebox.showerror('Error', f'No data for {player}')
            return
        output = (
            f'Points: {stats["points"]:.1f}\n'
            f'Rebounds: {stats["rebounds"]:.1f}\n'
            f'Assists: {stats["assists"]:.1f}\n'
            f'Steals: {stats["steals"]:.1f}\n'
            f'FG%: {stats["fg_pct"]:.3f}\n'
            f'FT%: {stats["ft_pct"]:.3f}'
        )
        self.stats_text.config(state='normal')
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert(tk.END, output)
        self.stats_text.config(state='disabled')


def main():
    app = BettingApp()
    app.mainloop()


if __name__ == '__main__':
    main()
