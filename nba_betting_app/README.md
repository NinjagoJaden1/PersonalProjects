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


Additional games can be added to improve the model. Sample player stats are
available in `data/sample_player_stats.csv`.
=======

Additional games can be added to improve the model. Sample player stats are
available in `data/sample_player_stats.csv`.
=======
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


## Streamlit Web App

If you prefer a web style interface, launch the Streamlit app:

```
streamlit run streamlit_app.py
```

The page lets you pick the home and away team from dropdown menus and tap the
"🔮 Predict" button. The result appears in a centered card with emoji styling so
it looks great even on mobile screens inside Visual Studio Code.

## Interactive App

An additional script, `app.py`, offers a small interactive menu where you can
choose teams or players and display the corresponding predictions. Run it with:

```
python app.py
```

You will then be prompted to select whether you want to predict a game outcome
or a player's stats. The data comes from the same sample CSV files mentioned
above and can be extended with more recent games.
=======


## Player Stats Usage

A second script, `player_predictor.py`, demonstrates a very naive approach to predicting individual player statistics. It loads a CSV of past player game logs and outputs the player's average points, rebounds, assists, steals and shooting percentages.

```
python player_predictor.py --data data/sample_player_stats.csv "LeBron James"
```

The prediction simply mirrors the player's historical averages in the sample data and is **not** meant for real betting use.


## Graphical App

For a simple graphical interface that works in Visual Studio Code, run `gui_app.py`:

```
python gui_app.py
```

This Tkinter-based window lets you choose teams or a player from dropdown menus
and view either a game win probability or the player's average stats.
=======
=======

