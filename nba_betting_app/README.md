# NBA Betting Predictor

This small project demonstrates simple NBA game and player predictions. Sample
CSV files in the `data` directory are generated from real 2023-24 season games.
Ratings are based on average point differential and a logistic function
converts rating difference to win probability.

## Refreshing sample data

Run `update_games.py` to download the entire 2023‑24 schedule and all player
box scores from the [balldontlie](https://www.balldontlie.io) API:


```bash
- `app.py` – basic text interface (games and player stats)
- `gui_app.py` – Tkinter window with tabs for games and players
- `streamlit_app.py` – simple web interface supporting both modes

```
date,home_team,away_team,home_points,away_points
```


Additional games can be added to improve the model. The repository includes
several matchups featuring current NBA teams along with sample player game logs
in `data/sample_player_stats.csv`.

### Updating game data

The script `update_data.py` downloads games and basic player box scores from the
[balldontlie](https://www.balldontlie.io) API. New rows are appended to
`data/nba_games.csv` and `data/player_stats.csv` while avoiding duplicates. The
script shows progress with `tqdm` and is configured to run every day at 4:00 AM
if you leave it running:

```
python update_data.py
```

This requires an internet connection and may take a few minutes on the first
run because it fetches the entire current season.

### Refreshing sample data

If you only want a small dataset for demonstration, run `update_games.py`.
It downloads the ten latest games from the 2023 season using the
[balldontlie](https://www.balldontlie.io) API and writes them to
`data/sample_games.csv` and the accompanying player stats to
`data/sample_player_stats.csv`.
=======

Additional games can be added to improve the model. Sample player stats are
available in `data/sample_player_stats.csv`.
=======

Additional games can be added to improve the model. Sample player stats are
available in `data/sample_player_stats.csv`.
=======
Additional games can be added to improve the model.




## Usage



This will output the predicted probability that the home team (first argument)
beats the away team (second argument) based on the historical data.

The model is intentionally simple and meant only as an example. For real sports
betting use, more sophisticated statistics and much larger datasets would be
required.


## Interactive App

An additional script, `app.py`, offers a small interactive menu where you can
choose teams or players and display the corresponding predictions. Run it with:

```
python app.py

```

## Command line usage

Predict a matchup by passing the home and away teams:

```bash
python predictor.py "Denver Nuggets" "Los Angeles Lakers"
```

The script prints each team's rating, the difference and the resulting win
probability.

## Interactive helpers

- `app.py` – basic text interface
- `gui_app.py` – Tkinter window
- `streamlit_app.py` – simple web interface

All interfaces use the same sample CSV files and list every NBA team so you can
experiment with predictions.
