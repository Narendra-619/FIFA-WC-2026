import streamlit as st


import streamlit as st
from predictor import predict_neutral


import pandas as pd

st.set_page_config(
    page_title="FIFA World Cup 2026 Predictor",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FIFA World Cup 2026 Predictor")

teams_df = pd.read_csv(
    "data/final_team_features.csv"
)

teams = sorted(
    teams_df["Nation"].unique()
)

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox(
        "Select Team 1",
        teams
    )

with col2:
    team2 = st.selectbox(
        "Select Team 2",
        teams,
        index=1
    )

if st.button("Predict Match"):

    result = predict_neutral(
        team1,
        team2
    )

    st.subheader("Prediction")

    st.metric(
        team1,
        f"{result[0] * 100:.2f}%"
        )

    st.metric(
        "Draw",
        f"{result[1] * 100:.2f}%"
    )

    st.metric(
    team2,
    f"{result[2] * 100:.2f}%"
    )
    