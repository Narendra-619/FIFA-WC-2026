import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="World Cup 2026 Predictions",
    page_icon="🏆",
    layout="wide"
)

# Load Data
df = pd.read_csv(
    "data/wc2026_simulation_results_v2.csv",
    encoding="latin1"
)

# Sort by World Cup winning probability
df = df.sort_values("Win_%", ascending=False)

st.title("🏆 FIFA World Cup 2026 Tournament Predictions")
st.subheader("Knockout Stage & Title Probabilities")

# -----------------------------
# Top 10 Favorites
# -----------------------------
st.markdown("## 🌟 Top 10 Favorites")

top10 = df.head(10)

st.bar_chart(
    top10.set_index("Nation")["Win_%"]
)

# -----------------------------
# Team Search
# -----------------------------
st.markdown("## 🔍 Team Analysis")

selected_team = st.selectbox(
    "Select a Team",
    df["Nation"]
)

team = df[df["Nation"] == selected_team].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🏆 Win World Cup", f"{team['Win_%']:.2f}%")
    st.metric("🥈 Reach Final", f"{team['Final_%']:.2f}%")

with col2:
    st.metric("🥉 Reach Semi Final", f"{team['Semi_Final_%']:.2f}%")
    st.metric("🏅 Reach Quarter Final", f"{team['Quarter_Final_%']:.2f}%")

with col3:
    st.metric("⚽ Reach Round of 16", f"{team['Round_of_16_%']:.2f}%")
    st.metric("🎯 Reach Round of 32", f"{team['Round_of_32_%']:.2f}%")

st.metric(
    "❌ Group Stage Exit",
    f"{team['Group_Exit_%']:.2f}%"
)

# -----------------------------
# Full Tournament Table
# -----------------------------
st.markdown("## 📊 All 48 Teams")

display_df = df[
    [
        "Rank",
        "Nation",
        "Win_%",
        "Final_%",
        "Semi_Final_%",
        "Quarter_Final_%",
        "Round_of_16_%",
        "Round_of_32_%",
        "Group_Exit_%"
    ]
]

display_df.columns = [
    "Rank",
    "Team",
    "Win %",
    "Final %",
    "Semi Final %",
    "Quarter Final %",
    "Round of 16 %",
    "Round of 32 %",
    "Group Exit %"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Probability Cards
# -----------------------------
st.markdown("## 🏆 World Cup Winner Probabilities")

for i in range(0, len(df), 4):

    cols = st.columns(4)

    for j, (_, row) in enumerate(df.iloc[i:i+4].iterrows()):

        with cols[j]:

            st.metric(
                row["Nation"],
                f"{row['Win_%']:.2f}%"
            )