import streamlit as st
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="World Cup 2026 | Prediction Report Card",
    page_icon="🏆",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/world_cup_2026_COMPLETE.csv", encoding="latin1")

    knockout_rounds = [
        "Round of 32", "Round of 16", "Quarter-finals",
        "Semi-finals", "Third Place", "Final"
    ]
    df["stage"] = df["group"].apply(
        lambda g: "Knockout" if g in knockout_rounds else "Group Stage"
    )
    df["correct"] = df["predicted_result"] == df["actual_result"]

    # Keep teamA / teamB as real columns (so we can filter/search by team),
    # but also build a single display string for the table itself.
    df["matchup"] = df["teamA"] + " vs " + df["teamB"]

    return df

df = load_data()

# -----------------------------
# Header
# -----------------------------
st.title("🏆 FIFA World Cup 2026 — Prediction Report Card")
st.caption("104 matches predicted before a ball was kicked. Here's how the model actually did.")

# -----------------------------
# Accuracy Scoreboard
# -----------------------------
overall_correct = int(df["correct"].sum())
overall_total = len(df)

group_df = df[df["stage"] == "Group Stage"]
ko_df = df[df["stage"] == "Knockout"]

group_correct, group_total = int(group_df["correct"].sum()), len(group_df)
ko_correct, ko_total = int(ko_df["correct"].sum()), len(ko_df)

st.markdown("## 📊 Prediction Accuracy")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(
        "Overall Accuracy",
        f"{overall_correct/overall_total:.1%}",
        f"{overall_correct} of {overall_total} correct"
    )
with c2:
    st.metric(
        "Group Stage",
        f"{group_correct/group_total:.1%}",
        f"{group_correct} of {group_total} correct"
    )
with c3:
    st.metric(
        "Knockout Stage",
        f"{ko_correct/ko_total:.1%}",
        f"{ko_correct} of {ko_total} correct"
    )

st.divider()

# -----------------------------
# Pre-Tournament Pick Accuracy
# -----------------------------
st.markdown("## 🔮 Pre-Tournament Pick Accuracy")
st.markdown(
    "Before the tournament, the top 5 picks to win it all were "
    "**France, Spain, Argentina, Brazil, England**. "
    "**4 of those 5** ended up in the actual semi-finals — only Brazil fell short."
)

preseason_top5 = ["France", "Spain", "Argentina", "Brazil", "England"]
actual_semifinalists = {"France", "Spain", "Argentina", "England"}

pick_cols = st.columns(5)
for col, team in zip(pick_cols, preseason_top5):
    hit = team in actual_semifinalists
    with col:
        st.metric(
            team,
            "✅ Reached Semis" if hit else "❌ Early Exit"
        )

st.caption("4 / 5 pre-tournament favorites confirmed → 80% hit rate")

st.divider()

# -----------------------------
# Filters
# -----------------------------
st.markdown("## 🔍 Match-by-Match Results")

f1, f2, f3 = st.columns([1.2, 1, 1])

with f1:
    stage_filter = st.multiselect(
        "Stage",
        options=sorted(df["stage"].unique()),
        default=sorted(df["stage"].unique())
    )

with f2:
    group_filter = st.multiselect(
        "Group / Round",
        options=list(df["group"].unique()),
        default=[]
    )

with f3:
    result_filter = st.radio(
        "Prediction result",
        options=["All", "Correct only", "Incorrect only"],
        horizontal=True
    )

all_teams = sorted(set(df["teamA"]).union(set(df["teamB"])))
team_filter = st.multiselect("Filter by team", options=all_teams, default=[])

filtered = df[df["stage"].isin(stage_filter)]

if group_filter:
    filtered = filtered[filtered["group"].isin(group_filter)]

if result_filter == "Correct only":
    filtered = filtered[filtered["correct"]]
elif result_filter == "Incorrect only":
    filtered = filtered[~filtered["correct"]]

if team_filter:
    filtered = filtered[
        filtered["teamA"].isin(team_filter) | filtered["teamB"].isin(team_filter)
    ]

filtered = filtered.sort_values("match_no")

# -----------------------------
# Results Table
# -----------------------------
display_df = filtered[[
    "match_no", "group", "date", "matchup",
    "predicted_result", "actual_result", "difference"
]].rename(columns={
    "match_no": "Match No",
    "group": "Group / Round",
    "date": "Date",
    "matchup": "Matchup",
    "predicted_result": "Predicted Result",
    "actual_result": "Actual Result",
    "difference": "Difference"
})

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Difference": st.column_config.NumberColumn(format="%.2f")
    }
)

st.caption(f"Showing {len(filtered)} of {len(df)} matches.")

st.divider()

# -----------------------------
# Optional: Accuracy by stage chart
# -----------------------------
st.markdown("## 📈 Accuracy Snapshot by Round")

by_round = (
    df.groupby("group")["correct"]
    .agg(["sum", "count"])
    .rename(columns={"sum": "Correct", "count": "Total"})
)
by_round["Accuracy %"] = (by_round["Correct"] / by_round["Total"] * 100).round(1)
by_round = by_round.reindex(
    [g for g in [
        "A","B","C","D","E","F","G","H","I","J","K","L",
        "Round of 32","Round of 16","Quarter-finals",
        "Semi-finals","Third Place","Final"
    ] if g in by_round.index]
)

st.bar_chart(by_round["Accuracy %"])

st.caption("Built from the pre-tournament simulation vs. final actual results — 104 matches tracked end to end.")