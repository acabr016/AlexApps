import streamlit as st
from collections import Counter
import pandas as pd
import os

CSV_FILE = "boardgame_votes.csv"
ADMIN_PASSWORD = "ClearItAll"  # Change to your password

# Initialize a session state variable to control refresh
if "refresh" not in st.session_state:
    st.session_state.refresh = False

def refresh_page():
    # Toggle the refresh flag to force reload UI elements below
    st.session_state.refresh = not st.session_state.refresh

# Load votes from CSV
if os.path.exists(CSV_FILE):
    votes_df = pd.read_csv(CSV_FILE)
else:
    votes_df = pd.DataFrame(columns=["Name", "Choice"])

food_options = [
    "Panda Express",
    "Wing Stop",
    "Marco's Pizza",
    "Ocha Thai",
    "Popeye's"
]

st.title("🍕 Board Game Night Food Poll 🎲")
st.subheader("Vote for your favorite food for the game night!")

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
        refresh_page()  # simulate refresh

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

if st.button("🔄 Refresh Results"):
    refresh_page()  # manually refresh by toggling state

st.subheader("🛠 Admin Panel")
admin_pass = st.text_input("Enter admin password:", type="password")
if st.button("Clear All Votes"):
    if admin_pass == ADMIN_PASSWORD:
        v
