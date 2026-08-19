import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="FIFA World Cup 2026",
    page_icon="🏆",
    layout="wide"
)

# Load Data
df = pd.read_csv(
    "data/group_probabilities.csv",
    encoding="latin1"
)

# Header
st.title("🏆 FIFA World Cup 2026 Predictor")
st.markdown(
    """
    ### Group Winner Probabilities
    Explore each group's chances of finishing in 1st place.
    """
)

st.divider()

groups = sorted(df["Group"].dropna().unique())

for i in range(0, len(groups), 4):

    cols = st.columns(4)

    for j, grp in enumerate(groups[i:i+4]):

        grp_df = (
            df[df["Group"] == grp]
            .sort_values("Probability", ascending=False)
        )

        with cols[j]:

            with st.container(border=True):

                st.markdown(
                    f"<h3 style='text-align:center;'>Group {grp}</h3>",
                    unsafe_allow_html=True
                )

                st.divider()

                for idx, (_, row) in enumerate(grp_df.iterrows()):

                    medal = ""

                    if idx == 0:
                        medal = "🥇"
                    elif idx == 1:
                        medal = "🥈"
                    elif idx == 2:
                        medal = "🥉"

                    st.metric(
                        label=f"{medal} {row['Team']}",
                        value=f"{row['Probability']:.2f}%"
                    )