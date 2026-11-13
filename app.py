import os
import pandas as pd
import plotly.express as px
import streamlit as st

OUT = "."
st.set_page_config(page_title="Pressure Players", layout="wide")

@st.cache_data
def load(name):
    p = os.path.join(OUT, name)
    return pd.read_csv(p) if os.path.exists(p) else None

top_bat, top_bowl = load("top_10_batters.csv"), load("top_10_bowlers.csv")
all_bat, all_bowl = load("all_batters.csv"), load("all_bowlers.csv")
summary = load("pressure_summary.csv")

st.title("SupeRR Selector S2: Most Reliable Players Under Pressure")
st.caption("High pressure = top 22.5% of balls by win-probability leverage. "
           "Rating = runs and wickets above context-expected, shrunk toward the player's own normal level.")

def player_tab(top, full, balls, rating, raw_p, raw_n, label):
    if top is None:
        st.error("Output CSVs not found. Run the analysis cells first.")
        return
    cols = [c for c in ["Rank", "player_name", balls, rating, "consistency", "top10_prob"] if c in top.columns]
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(f"Top 10 {label}")
        st.dataframe(top[cols], hide_index=True, use_container_width=True)
        st.download_button("Download CSV", top.to_csv(index=False),
                           f"top_10_{label.lower()}.csv", key=f"dl_{label}")
    with c2:
        fig = px.bar(top.sort_values(rating), x=rating, y="player_name", orientation="h")
        fig.update_layout(yaxis_title=None, height=400)
        st.plotly_chart(fig, use_container_width=True)
    if full is not None and raw_p in full.columns:
        st.subheader("Explorer")
        min_b = st.slider("Minimum pressure balls", 30, 300, 50, 10, key=f"s_{label}")
        d = full[full[balls] >= min_b].copy()
        fig = px.scatter(d, x=raw_n, y=raw_p, size=balls, hover_name="player_name",
                         labels={raw_n: "Rating in ordinary situations",
                                 raw_p: "Rating under pressure"})
        lo, hi = min(d[raw_n].min(), d[raw_p].min()), max(d[raw_n].max(), d[raw_p].max())
        fig.add_shape(type="line", x0=lo, y0=lo, x1=hi, y1=hi, line=dict(dash="dash"))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Above the dashed line = better under pressure than usual.")
        st.dataframe(d.sort_values(rating, ascending=False)
                       [["player_name", balls, raw_n, raw_p, rating]].head(25),
                     hide_index=True, use_container_width=True)

t1, t2, t3, t4 = st.tabs(["Batters", "Bowlers", "Pressure definition", "Method and limits"])
with t1:
    player_tab(top_bat, all_bat, "pressure_balls_faced", "shrunk_bat_rating",
               "raw_bat_rating_pressure", "raw_bat_rating_normal", "Batters")
with t2:
    player_tab(top_bowl, all_bowl, "pressure_balls_bowled", "shrunk_bowl_rating",
               "raw_bowl_rating_pressure", "raw_bowl_rating_normal", "Bowlers")
with t3:
    st.markdown("**Leverage** = WP x (1 - WP) x 120 / (balls remaining + 6), "
                "where WP is the batting side's win probability from a gradient-boosting model.")
    if summary is not None:
        st.dataframe(summary, hide_index=True, use_container_width=True)
    img = os.path.join(OUT, "pressure_distribution.png")
    if os.path.exists(img):
        st.image(img)
with t4:
    st.markdown("""
- Context-adjusted expected runs and wickets per ball; rating = actual minus expected.
- Shrinkage toward each player's own ordinary-situation rating (k = 40).
- Limitations: no fielding or ball-tracking data, small pressure samples, mixed IPL and T20I opposition strength.
""")
