# boardgame_food_poll.py
import streamlit as st
from collections import Counter
import pandas as pd
import os
import json

CSV_FILE = "boardgame_votes.csv"
CALENDAR_FILE = "boardgame_calendar.json"
ADMIN_PASSWORD = "ClearItAll"  # Change to your own secure password

# --- Session state workaround for refresh ---
if "refresh" not in st.session_state:
    st.session_state.refresh = False

def refresh_page():
    st.session_state.refresh = not st.session_state.refresh

# --- Load votes ---
if os.path.exists(CSV_FILE):
    votes_df = pd.read_csv(CSV_FILE)
else:
    votes_df = pd.DataFrame(columns=["Name", "Choice"])

# --- Load calendar ---
def load_calendar():
    if os.path.exists(CALENDAR_FILE):
        with open(CALENDAR_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "date": "2025-08-20",
            "games": "Catan, Carcassonne"
        }

def save_calendar(data):
    with open(CALENDAR_FILE, "w") as f:
        json.dump(data, f)

calendar_data = load_calendar()

# --- Food options ---
food_options = [
    "Panda Express",
    "Wing Stop",
    "Marco's Pizza",
    "Ocha Thai",
    "Popeye's"
]

# --- Page Title ---
st.title("🍕 Board Game Night Food Poll 🎲")
st.subheader("Vote for your favorite food for the game night!")

# --- User voting input ---
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
        refresh_page()

# --- Show votes and tally ---
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

# --- Manual refresh button ---
if st.button("🔄 Refresh Results"):
    refresh_page()

# --- Admin panel for clearing votes ---
st.subheader("🛠 Admin Panel")
admin_pass = st.text_input("Enter admin password:", type="password", key="admin_pass")

if st.button("Clear All Votes"):
    if admin_pass == ADMIN_PASSWORD:
        votes_df = pd.DataFrame(columns=["Name", "Choice"])
        votes_df.to_csv(CSV_FILE, index=False)
        st.warning("All votes have been cleared!")
        refresh_page()
    else:
        st.error("Incorrect password.")

# --- Upcoming Board Game Night calendar display ---
st.subheader("📅 Upcoming Board Game Night")

st.markdown(f"**Date:** {calendar_data['date']}")
st.markdown(f"**Games:** {calendar_data['games']}")

# --- Admin calendar editing ---
st.subheader("🛠 Calendar Admin Panel")
admin_pass_cal = st.text_input("Enter admin password to edit calendar:", type="password", key="cal_pass")

if admin_pass_cal == ADMIN_PASSWORD:
    new_date = st.date_input("Set next game night date:", pd.to_datetime(calendar_data['date']))
    new_games = st.text_area("Games to be played:", calendar_data['games'])

    if st.button("Save Calendar Updates"):
        updated_data = {
            "date": new_date.strftime("%Y-%m-%d"),
            "games": new_games
        }
        save_calendar(updated_data)
        st.success("Calendar updated!")
        refresh_page()
elif admin_pass_cal:
    st.error("Incorrect password for calendar admin.")
