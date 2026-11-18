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

PAKISTANI_PLAYERS = {
    "Asif Ali",
    "Mohammad Rizwan",
    "Iftikhar Ahmed",
    "Sahibzada Farhan",
    "Salman Agha",
    "Khushdil Shah",
    "Faheem Ashraf",
    "Tayyab Tahir",
    "Mohammad Haris",
    "Muhammad Irfan",
    "Usman Khan",
    "Hasan Nawaz",
    "KM Asif",
    "Shaheen Afridi",
    "Mohammad Hasnain",
    "Haris Rauf",
    "Saim Ayub",
    "Mohammad Wasim",
    "Abbas Afridi",
    "Naseem Shah",
    "Shahnawaz Dhani",
    "Abrar Ahmed",
    "Salman Mirza",
    "Haider Ali",
}

IPL_2027_RETAINED_PLAYERS = {
    "Abdul Samad",
    "Abhishek Sharma",
    "Aiden Markram",
    "Akeal Hosein",
    "Angkrish Raghuvanshi",
    "Aniket Verma",
    "Anshul Kamboj",
    "Anuj Rawat",
    "Anukul Roy",
    "Arshad Khan",
    "Arshdeep Singh",
    "Ashok Sharma",
    "Ashutosh Sharma",
    "Ashwani Kumar",
    "Axar Patel",
    "Ayush Badoni",
    "Azmatullah Omarzai",
    "Ben Dwarshuis",
    "Bhuvneshwar Kumar",
    "Brijesh Sharma",
    "Brydon Carse",
    "Cameron Green",
    "Corbin Bosch",
    "Dasun Shanaka",
    "David Miller",
    "Devdutt Padikkal",
    "Dewald Brevis",
    "Dhruv Jurel",
    "Digvesh Rathi",
    "Donovan Ferreira",
    "Eshan Malinga",
    "Glenn Phillips",
    "Hardik Pandya",
    "Harpreet Brar",
    "Harshal Patel",
    "Harshit Rana",
    "Heinrich Klaasen",
    "Ishan Kishan",
    "Jacob Duffy",
    "Jamie Overton",
    "Jason Holder",
    "Jasprit Bumrah",
    "Jitesh Sharma",
    "Jofra Archer",
    "Jos Buttler",
    "Josh Hazlewood",
    "Josh Inglis",
    "Kagiso Rabada",
    "Kartik Sharma",
    "Kartik Tyagi",
    "Khaleel Ahmed",
    "Krunal Pandya",
    "Kuldeep Yadav",
    "Kyle Jamieson",
    "Liam Livingstone",
    "Lokesh Rahul",
    "Lungi Ngidi",
    "Manish Pandey",
    "Marco Jansen",
    "Marcus Stoinis",
    "Mayank Yadav",
    "Mitchell Marsh",
    "Mitchell Santner",
    "Mohammed Shami",
    "Mohammed Siraj",
    "Mohsin Khan",
    "Mukesh Choudhary",
    "Mukesh Kumar",
    "Mukul Choudhary",
    "Naman Dhir",
    "Namboori Tilak Varma",
    "Nandre Burger",
    "Nathan Ellis",
    "Nicholas Pooran",
    "Noor Ahmad",
    "Nuwan Thushara",
    "Patrick Cummins",
    "Phil Salt",
    "Prabhsimran Singh",
    "Praful Hinge",
    "Prasidh Krishna",
    "Prince Yadav",
    "Quinton de Kock",
    "Rahul Chahar",
    "Rahul Tewatia",
    "Rajat Patidar",
    "Ramandeep Singh",
    "Rashid Khan",
    "Rasikh Salam",
    "Ravi Bishnoi",
    "Ravindra Jadeja",
    "Rinku Singh",
    "Rishabh Pant",
    "Riyan Parag",
    "Rohit Sharma",
    "Romario Shepherd",
    "Rovman Powell",
    "Ruturaj Gaikwad",
    "Sai Kishore",
    "Sai Sudharsan",
    "Sakib Hussain",
    "Salil Arora",
    "Sam Curran",
    "Sameer Rizvi",
    "Sandeep Sharma",
    "Sanju Samson",
    "Sarfaraz Khan",
    "Shahbaz Ahmed",
    "Shardul Thakur",
    "Shashank Singh",
    "Sherfane Rutherford",
    "Shivam Dube",
    "Shreyas Iyer",
    "Shubham Dubey",
    "Shubman Gill",
    "Sunil Narine",
    "Suryakumar Yadav",
    "Suyash Sharma",
    "Tim David",
    "Tristan Stubbs",
    "Vaibhav Arora",
    "Varun Chakravarthy",
    "Venkatesh Iyer",
    "Vipraj Nigam",
    "Virat Kohli",
    "Vyshak Kumar",
    "Washington Sundar",
    "William Jacks",
    "Xavier Bartlett",
    "Yash Dayal",
    "Yash Thakur",
    "Yashasvi Jaiswal",
    "Yuzvendra Chahal",
}

RETIRED_PLAYERS = {
    "Ajinkya Rahane",
    "Ambati Rayudu",
    "Amit Mishra",
    "Andre Russell",
    "Dinesh Karthik",
    "Dwayne Bravo",
    "Karn Sharma",
    "Kieron Pollard",
    "Mahendra Singh Dhoni",
    "Ravichandran Ashwin",
    "Shikhar Dhawan",
    "Vijay Shankar",
}

PLAYERS_38_OR_OLDER = {
    "Adil Rashid",
    "Angelo Mathews",
    "Chris Jordan",
    "Dawid Malan",
    "David Warner",
    "Faf du Plessis",
    "Glenn Maxwell",
    "Ishant Sharma",
    "Matthew Wade",
    "Mohammad Mahmudullah",
    "Mohammad Nabi",
    "Moeen Ali",
    "Shakib Al Hasan",
    "Sikandar Raza",
    "Sunil Narine",
    "Ehsan Khan",
    "Umesh Yadav",
}

def exclude_ineligible_players(df):
    if df is None or "player_name" not in df.columns:
        return df
    excluded = (
        PAKISTANI_PLAYERS
        | IPL_2027_RETAINED_PLAYERS
        | RETIRED_PLAYERS
        | PLAYERS_38_OR_OLDER
    )
    filtered = df[~df["player_name"].isin(excluded)].copy()
    if "Rank" in filtered.columns:
        filtered["Rank"] = range(1, len(filtered) + 1)
    return filtered


def build_top_ten(full, previous_top, balls, rating):
    if full is None:
        return exclude_ineligible_players(previous_top)

    pressure_matches = (
        previous_top.set_index("player_name")["pressure_matches"].to_dict()
        if previous_top is not None and "pressure_matches" in previous_top.columns
        else {}
    )
    eligible = full[full[balls] >= 30]
    top = eligible.nlargest(10, rating)
    top = top.copy()
    top.insert(6, "pressure_matches", top["player_name"].map(pressure_matches))
    top["Rank"] = range(1, len(top) + 1)
    return top


all_bat = exclude_ineligible_players(load("all_batters.csv"))
all_bowl = exclude_ineligible_players(load("all_bowlers.csv"))
top_bat = build_top_ten(
    all_bat, load("top_10_batters.csv"),
    "pressure_balls_faced", "shrunk_bat_rating",
)
top_bowl = build_top_ten(
    all_bowl, load("top_10_bowlers.csv"),
    "pressure_balls_bowled", "shrunk_bowl_rating",
)
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
        min_b = st.slider("Minimum pressure balls", 30, 300, 30, 10, key=f"s_{label}")
        d = full[full[balls] >= min_b].copy()
        fig = px.scatter(d, x=raw_n, y=raw_p, size=balls, hover_name="player_name",
                         labels={raw_n: "Rating in ordinary situations",
                                 raw_p: "Rating under pressure"})
        lo, hi = min(d[raw_n].min(), d[raw_p].min()), max(d[raw_n].max(), d[raw_p].max())
        fig.add_shape(type="line", x0=lo, y0=lo, x1=hi, y1=hi, line=dict(dash="dash"))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Above the dashed line = better under pressure than usual.")
        st.dataframe(d.sort_values(rating, ascending=False)
                       [["player_name", balls, raw_n, raw_p, rating]],
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
