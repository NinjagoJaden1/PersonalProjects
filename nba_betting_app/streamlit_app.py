import math
import streamlit as st
from predictor import load_games, compute_team_ratings

DATA_PATH = 'data/sample_games.csv'


def train_logistic_regression(features, labels, lr=0.001, epochs=1000):
    """Train a simple logistic regression via gradient descent."""
    w0 = 0.0
    w1 = 0.0
    n = len(features)
    for _ in range(epochs):
        grad0 = 0.0
        grad1 = 0.0
        for x, y in zip(features, labels):
            z = w0 + w1 * x
            y_pred = 1 / (1 + math.exp(-z))
            error = y_pred - y
            grad0 += error
            grad1 += error * x
        w0 -= lr * grad0 / n
        w1 -= lr * grad1 / n
    return w0, w1


def logistic_predict(w0, w1, x):
    return 1 / (1 + math.exp(-(w0 + w1 * x)))


# Load data and prepare model
_games = load_games(DATA_PATH)
_features = [g['home_points'] - g['away_points'] for g in _games]
_labels = [1 if g['home_points'] > g['away_points'] else 0 for g in _games]
_w0, _w1 = train_logistic_regression(_features, _labels)
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
        prob = logistic_predict(_w0, _w1, diff)
        winner = home_team if prob >= 0.5 else away_team
        st.markdown(
            f"<div style='margin-top:20px; padding:20px; text-align:center; "
            f"background-color:#f2f2f2; border-radius:10px;'>"
            f"<h2>{winner} 🏆</h2>"
            f"<p>Win probability for {home_team}: {prob:.1%}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

