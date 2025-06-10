import math
import streamlit as st
from predictor import load_games, compute_team_ratings

from player_predictor import load_player_stats, compute_averages
=======

from teams import ALL_TEAMS

DATA_PATH = 'data/sample_games.csv'
STATS_PATH = 'data/sample_player_stats.csv'


def logistic(x, k=0.1):
    """Simple logistic function for rating difference."""
    return 1 / (1 + math.exp(-k * x))


# Load data and prepare model
_games = load_games(DATA_PATH)
_ratings = compute_team_ratings(_games)

_player_data = load_player_stats(STATS_PATH)
_player_avgs = compute_averages(_player_data)
_players = sorted(_player_avgs.keys())
_teams = sorted(ALL_TEAMS)

st.set_page_config(page_title='NBA Predictor', page_icon='🏀')
st.markdown("<h1 style='text-align:center;'>🏀 NBA Predictor</h1>", unsafe_allow_html=True)

mode = st.radio('Select mode', ['Game Prediction', 'Player Stats'])

if mode == 'Game Prediction':
    home_team = st.selectbox('🏠 Home Team', _teams)
    away_team = st.selectbox('🚌 Away Team', _teams, index=1)

    predict = st.button('🔮 Predict', use_container_width=True)

    if predict:
        if home_team == away_team:
            st.warning('Choose two different teams.')
        else:
            diff = _ratings.get(home_team, 0) - _ratings.get(away_team, 0)
            prob = logistic(diff)
            winner = home_team if prob >= 0.5 else away_team
            reason = (
                f"Home rating {_ratings.get(home_team,0):.2f}, "
                f"Away rating {_ratings.get(away_team,0):.2f}, diff {diff:.2f}"
            )
            st.markdown(
                f"<div style='margin-top:20px; padding:20px; text-align:center; "
                f"background-color:#f2f2f2; border-radius:10px; color:black;'>"
                f"<h2 style='color:black;'>{winner} 🏆</h2>"
                f"<p style='color:black;'>{reason}</p>"
                f"<p style='color:black;'>Win probability for {home_team}: {prob:.1%}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
else:
    player = st.selectbox('Player', _players)
    show = st.button('📈 Show Stats', use_container_width=True)
    if show:
        stats = _player_avgs.get(player)
        if not stats:
            st.warning('No data for player')
        else:
            st.markdown(
                f"<div style='margin-top:20px; padding:20px; text-align:center; "
                f"background-color:#f2f2f2; border-radius:10px; color:black;'>"
                f"<h3 style='color:black;'>{player}</h3>"
                f"<p style='color:black;'>Points: {stats['points']:.1f}</p>"
                f"<p style='color:black;'>Rebounds: {stats['rebounds']:.1f}</p>"
                f"<p style='color:black;'>Assists: {stats['assists']:.1f}</p>"
                f"<p style='color:black;'>Steals: {stats['steals']:.1f}</p>"
                f"<p style='color:black;'>FG%: {stats['fg_pct']:.3f}</p>"
                f"<p style='color:black;'>FT%: {stats['ft_pct']:.3f}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
=======
_teams = sorted(ALL_TEAMS)

st.set_page_config(page_title='NBA Predictor', page_icon='🏀')
st.markdown("<h1 style='text-align:center;'>🏀 NBA Game Predictor</h1>", unsafe_allow_html=True)

home_team = st.selectbox('🏠 Home Team', _teams)
away_team = st.selectbox('🚌 Away Team', _teams, index=1)

predict = st.button('🔮 Predict', use_container_width=True)

if predict:
    if home_team == away_team:
        st.warning('Choose two different teams.')
    else:
        diff = _ratings.get(home_team, 0) - _ratings.get(away_team, 0)
        prob = logistic(diff)
        winner = home_team if prob >= 0.5 else away_team
        reason = (
            f"Home rating {_ratings.get(home_team,0):.2f}, "
            f"Away rating {_ratings.get(away_team,0):.2f}, diff {diff:.2f}"
        )
        st.markdown(
            f"<div style='margin-top:20px; padding:20px; text-align:center; "
            f"background-color:#f2f2f2; border-radius:10px; color:black;'>"
            f"<h2 style='color:black;'>{winner} 🏆</h2>"
            f"<p style='color:black;'>{reason}</p>"
            f"<p style='color:black;'>Win probability for {home_team}: {prob:.1%}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )


