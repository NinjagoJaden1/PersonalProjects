import math
import streamlit as st
from predictor import load_games, compute_team_ratings

DATA_PATH = 'data/sample_games.csv'


def logistic(x, k=0.1):
    """Simple logistic function for rating difference."""
    return 1 / (1 + math.exp(-k * x))


# Load data and prepare model
_games = load_games(DATA_PATH)
_ratings = compute_team_ratings(_games)
_teams = sorted({g['home_team'] for g in _games} | {g['away_team'] for g in _games})

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
        st.markdown(
    f"<div style='margin-top:20px; padding:20px; text-align:center; "
    f"background-color:#f2f2f2; border-radius:10px; color:black;'>"
    f"<h2 style='color:black;'>{winner} 🏆</h2>"
    f"<p style='color:black;'>Win probability for {home_team}: {prob:.1%}</p>"
    f"</div>",
    unsafe_allow_html=True,
)

