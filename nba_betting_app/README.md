# NBA Betting Predictor

This small project demonstrates simple NBA game and player predictions. Sample
CSV files in the `data` directory are generated from real 2023-24 season games.
Ratings are based on average point differential and a logistic function
converts rating difference to win probability.

## Refreshing sample data

Run `update_games.py` to download every game of the season (all 1230 contests)
along with player box scores from the
[balldontlie](https://www.balldontlie.io) API:

```bash
python update_games.py
```
Add `--season YEAR` to fetch a different season.

## Command line usage

Predict a matchup by passing the home and away teams:

```bash
python predictor.py "Denver Nuggets" "Los Angeles Lakers"
```

The script prints each team's rating, the difference and the resulting win
probability.

## Interactive helpers

- `app.py` – basic text interface (games and player stats)
- `gui_app.py` – Tkinter window with tabs for games and players
- `streamlit_app.py` – simple web interface supporting both modes

All interfaces use the same sample CSV files and list every NBA team so you can
experiment with predictions.
