# file: boardgame_food_poll.py
import streamlit as st
from collections import Counter
import pandas as pd
import os
import time

# --- Settings ---
CSV_FILE = "boardgame_votes.csv"
ADMIN_PASSWORD = "letmein"  # Change this to your own secure password
REFRESH_INTERVAL = 10  # seconds

# --- Auto-refresh ---
st_autorefresh = st.experimental_rerun  # for newer versions
st_autorefresh = st.experimental_rerun
st.set_page_config(page_title="Board Game Night Food Poll", layout="centered")
st_autorefresh = st_autorefresh

st_autorefresh = st_autorefresh
st_autorefresh = st_autorefresh

st_autorefresh = st_autorefresh
st_autorefresh = st_autorefresh

# Streamlit's built-in autorefresh
st_autorefresh = st_autorefresh

st_autorefresh = st_autorefresh

# --- Load votes ---
if os.path.exists(CSV_FILE):
    votes_df = pd.read_csv(CSV_FILE)
else:
    votes_df = pd.DataFrame(columns=["Name", "Choice"])

# --- Food options ---
food_options = [
    "Panda Express",
    "Wing Stop",
    "Marco's Pizza",
    "Ocha Thai",
    "Popeye's"
]

st.title("🍕 Board Game Night Food Poll 🎲")
st.caption(f"(Auto-refreshes every {REFRESH_INTERVAL} seconds)")

# --- User vote input ---
username = st.text_input("Enter your name:")

if username.strip():
    if username in votes_df["Name"].values:
        current_choice = votes_df.loc[votes_df["Name"] == username, "Choice"].values[0]
    else:
        current_choice = food_options[0]

    food_choice = st.radio("Choose one:", food_options, index=food_options.index(current_choice))

    if st.button("Submit / Update Vote"):
        if username in votes_df["Name"].values:
            votes_df.loc[votes_df["Name"] == username, "Choice"] = food_choice
        else:
            votes_df = pd.concat(
                [votes_df, pd.DataFrame({"Name": [username], "Choice": [food_choice]})],
                ignore_index=True
            )
        votes_df.to_csv(CSV_FILE, index=False)
        st.success(f"{username}, your vote for {food_choice} has been recorded ✅")

# --- Display results ---
if not votes_df.empty:
    st.subheader("📋 Everyone's Votes")
    st.dataframe(votes_df)

    st.subheader("📊 Current Results")
    counts = Counter(votes_df["Choice"])
    st.table([[food, count] for food, count in counts.items()])

    max_votes = max(counts.values())
    popular_choices = [food for food, count in counts.items() if count == max_votes]
    st.markdown(f"**🥇 Most Popular:** {', '.join(popular_choices)} ({max_votes} votes)")
else:
    st.info("No votes yet. Be the first to choose!")

# --- Admin clear votes ---
with st.expander("🔑 Admin Controls"):
    admin_pass = st.text_input("Enter admin password:", type="password")
    if st.button("Clear All Votes"):
        if admin_pass == ADMIN_PASSWORD:
            votes_df = pd.DataFrame(columns=["Name", "Choice"])
            votes_df.to_csv(CSV_FILE, index=False)
            st.success("✅ All votes have been cleared.")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect password. Access denied.")

# --- Auto-refresh every REFRESH_INTERVAL seconds ---
st.experimental_singleton.clear()
st_autorefresh = st.experimental_rerun
st_autorefresh
