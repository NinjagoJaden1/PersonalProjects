import math
import streamlit as st
import pandas as pd
from predictor import (
    load_games,
    compute_team_ratings,
    compute_team_point_avgs,

    compute_team_players,


    predict_final_score,
)
from player_predictor import load_player_stats, compute_averages
from teams import ALL_TEAMS

GAMES_PATH = 'data/sample_games.csv'
STATS_PATH = 'data/sample_player_stats.csv'


def logistic(x, k=0.1):
    return 1 / (1 + math.exp(-k * x))


# === CACHED LOADERS ===
@st.cache_data
def get_games_and_ratings():
    games = load_games(GAMES_PATH)

    # ❌ Remove or comment this
    # ratings = compute_team_ratings(games, trade_date=None)
    # avgs = compute_team_point_avgs(games, trade_date=None)

    # ✅ Use this version instead
    ratings = compute_team_ratings(games)
    avgs = compute_team_point_avgs(games)

    return games, ratings, avgs

@st.cache_data
def get_player_stats():
    stats = load_player_stats(STATS_PATH)
    averages = compute_averages(stats)
    team_players = compute_team_players(stats)
    return stats, averages, team_players


# === PAGE SETUP ===
st.set_page_config(page_title='NBA Predictor', page_icon='🏀')
st.markdown("<h1 style='text-align:center;'>🏀 NBA Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color: gray;'>by Jaden Cheung</h4>", unsafe_allow_html=True)
mode = st.selectbox('Prediction Type', ['Game Outcome', 'Player Averages'])

# === GAME OUTCOME ===
if mode == 'Game Outcome':
    games, ratings, team_avgs = get_games_and_ratings()

    _, _, team_players = get_player_stats()


    teams = sorted(ALL_TEAMS)

    home_team = st.selectbox('🏠 Home Team', teams)
    away_team = st.selectbox('🚌 Away Team', teams, index=1)

    if st.button('🔮 Predict', use_container_width=True):
        if home_team == away_team:
            st.warning('Choose two different teams.')
        else:
            diff = ratings.get(home_team, 0) - ratings.get(away_team, 0)
            prob = logistic(diff)
            home_score, away_score = predict_final_score(home_team, away_team, team_avgs)
            winner = home_team if prob >= 0.5 else away_team
            explanation = (
                f"{winner} are predicted to win because their rating is higher "
                f"than the opponent's by {abs(diff):.2f} points, based on season performance."
            )

            home_players = ", ".join(team_players.get(home_team, []))
            away_players = ", ".join(team_players.get(away_team, []))
            st.markdown(
                f"<div style='margin-top:20px; padding:20px; text-align:center; "
                f"background-color:#f2f2f2; border-radius:10px; color:black;'>"
                f"<h2 style='color:black;'>{winner} 🏆</h2>"
                f"<p style='color:black;'>{explanation}</p>"
                f"<p style='color:black;'>Win probability for {home_team}: {prob:.1%}</p>"
                f"<p style='color:black;'>Predicted score: {home_team} {home_score} - {away_team} {away_score}</p>"

                f"<p style='color:black;'>Players {home_team}: {home_players}</p>"
                f"<p style='color:black;'>Players {away_team}: {away_players}</p>"


                f"</div>",
                unsafe_allow_html=True,
            )

            past_games = [
                g for g in games
                if {g['home_team'], g['away_team']} == {home_team, away_team}
            ]
            if past_games:
                st.subheader("📊 Past Matchups Between These Teams")
                st.dataframe(
                    pd.DataFrame(past_games).sort_values("date", ascending=False).reset_index(drop=True),
                    use_container_width=True
                )
            else:
                st.info("No past matchups between these teams found in the data.")

# === PLAYER AVERAGES ===
elif mode == 'Player Averages':
    stats, player_avgs, _ = get_player_stats()
    players = sorted(player_avgs.keys())
    player = st.selectbox('Player', players)

    if st.button('🔮 Predict', use_container_width=True):
        stats = player_avgs.get(player)
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
