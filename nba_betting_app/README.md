# NBA Betting Predictor

This simple command line app loads past NBA game results from a CSV file and
computes a basic rating for each team based on average point differential.
Predictions for upcoming games are generated using these ratings and a logistic
function to produce a win probability for the home team.

## Data

Sample data is provided in `data/sample_games.csv`. The CSV should contain the
following columns:

```
date,home_team,away_team,home_points,away_points
```

Additional games can be added to improve the model.

## Usage

```
python predictor.py --data data/sample_games.csv "Lakers" "Bulls"
```

This will output the predicted probability that the home team (first argument)
beats the away team (second argument) based on the historical data.

The model is intentionally simple and meant only as an example. For real sports
betting use, more sophisticated statistics and much larger datasets would be
required.
