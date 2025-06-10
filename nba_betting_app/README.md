# NBA Betting Predictor

This small project demonstrates simple NBA game and player predictions. Sample
CSV files in the `data` directory contain a few results from the 2023-24
season. Ratings are based on average point differential and a logistic function
converts rating difference to win probability.

## Refreshing sample data

Run `update_games.py` to download the ten latest games and box scores from the
[balldontlie](https://www.balldontlie.io) API:

```bash
python update_games.py
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
