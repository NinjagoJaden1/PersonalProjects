import math
import streamlit as st
from predictor import load_games, compute_team_ratings
from player_predictor import load_player_stats, compute_averages
from teams import ALL_TEAMS

GAMES_PATH = 'data/sample_games.csv'
STATS_PATH = 'data/sample_player_stats.csv'


def logistic(x, k=0.1):
    """Simple logistic function for rating difference."""
    return 1 / (1 + math.exp(-k * x))


# Load data and prepare model
_games = load_games(GAMES_PATH)
_ratings = compute_team_ratings(_games)
_stats = load_player_stats(STATS_PATH)
_player_avgs = compute_averages(_stats)
_teams = sorted(ALL_TEAMS)
_players = sorted(_player_avgs.keys())

st.set_page_config(page_title='NBA Predictor', page_icon='🏀')
st.markdown("<h1 style='text-align:center;'>🏀 NBA Predictor</h1>", unsafe_allow_html=True)

mode = st.selectbox('Prediction Type', ['Game Outcome', 'Player Averages'])

if mode == 'Game Outcome':
    home_team = st.selectbox('🏠 Home Team', _teams)
    away_team = st.selectbox('🚌 Away Team', _teams, index=1)

    if st.button('🔮 Predict', use_container_width=True):
        if home_team == away_team:
            st.warning('Choose two different teams.')
        else:
            diff = _ratings.get(home_team, 0) - _ratings.get(away_team, 0)
            prob = logistic(diff)
            winner = home_team if prob >= 0.5 else away_team
            explanation = (
                f"{winner} are predicted to win because their rating is higher "
                f"than the opponent's by {abs(diff):.2f} points, based on season performance."
            )
            st.markdown(
                f"<div style='margin-top:20px; padding:20px; text-align:center; "
                f"background-color:#f2f2f2; border-radius:10px; color:black;'>"
                f"<h2 style='color:black;'>{winner} 🏆</h2>"
                f"<p style='color:black;'>{explanation}</p>"
                f"<p style='color:black;'>Win probability for {home_team}: {prob:.1%}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
elif mode == 'Player Averages':
    player = st.selectbox('Player', _players)
    if st.button('🔮 Predict', use_container_width=True):
        stats = _player_avgs.get(player)
        if not stats:
            st.warning('No data for that player.')
        else:
            st.markdown(
                f"<div style='margin-top:20px; padding:20px; text-align:center; "
                f"background-color:#f2f2f2; border-radius:10px; color:black;'>"
                f"<h3 style='color:black;'>{player}</h3>"
                f"<p style='color:black;'>Points: {stats['points']:.1f}</p>"
                f"<p style='color:black;'>Rebounds: {stats['rebounds']:.1f}</p>"
                f"<p style='color:black;'>Assists: {stats['assists']:.1f}</p>"
                f"<p style='color:black;'>Steals: {stats['steals']:.1f}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

