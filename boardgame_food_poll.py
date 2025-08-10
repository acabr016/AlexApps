# file: boardgame_food_poll.py
import streamlit as st
from collections import Counter
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh  # ✅ Import correct auto-refresh

# CSV file to store votes
CSV_FILE = "boardgame_votes.csv"
ADMIN_PASSWORD = "ClearItAll"  # Change this to your own password

# Auto-refresh every 5 seconds (5000 ms)
st_autorefresh(interval=5000, key="refresh")

# Load votes from CSV if it exists
if os.path.exists(CSV_FILE):
    votes_df = pd.read_csv(CSV_FILE)
else:
    votes_df = pd.DataFrame(columns=["Name", "Choice"])

# Food options
food_options = [
    "Panda Express",
    "Wing Stop",
    "Marco's Pizza",
    "Ocha Thai",
    "Popeye's"
]

st.title("🍕 Board Game Night Food Poll 🎲")
st.subheader("Vote for your favorite food for the game night!")

# User name input
username = st.text_input("Enter your name:")

# Only show voting options if name is entered
if username.strip():
    # Preselect user's previous choice if they have voted
    if username in votes_df["Name"].values:
        current_choice = votes_df.loc[votes_df["Name"] == username, "Choice"].values[0]
    else:
        current_choice = food_options[0]

    # Voting selection
    food_choice = st.radio("Choose one:", food_options, index=food_options.index(current_choice))

    # Submit / Update button
    if st.button("Submit / Update Vote"):
        if username in votes_df["Name"].values:
            # Update existing vote
            votes_df.loc[votes_df["Name"] == username, "Choice"] = food_choice
        else:
            # Add new vote
            votes_df = pd.concat(
                [votes_df, pd.DataFrame({"Name": [username], "Choice": [food_choice]})],
                ignore_index=True
            )

        # Save to CSV
        votes_df.to_csv(CSV_FILE, index=False)
        st.success(f"{username}, your vote for {food_choice} has been recorded ✅")
        st.experimental_rerun()

# Show everyone's votes if there are any
if not votes_df.empty:
    st.subheader("📋 Everyone's Votes")
    st.dataframe(votes_df)

    # Show tally
    st.subheader("📊 Current Results")
    counts = Counter(votes_df["Choice"])
    st.table([[food, count] for food, count in counts.items()])

    # Most popular choice(s)
    max_votes = max(counts.values())
    popular_choices = [food for food, count in counts.items() if count == max_votes]
    st.markdown(f"**🥇 Most Popular:** {', '.join(popular_choices)} ({max_votes} votes)")

else:
    st.info("No votes yet. Be the first to choose!")

# Admin controls
st.subheader("🛠 Admin Panel")
admin_pass = st.text_input("Enter admin password:", type="password")
if st.button("Clear All Votes"):
    if admin_pass == ADMIN_PASSWORD:
        votes_df = pd.DataFrame(columns=["Name", "Choice"])
        votes_df.to_csv(CSV_FILE, index=False)
        st.warning("All votes have been cleared!")
        st.experimental_rerun()
    else:
        st.error("Incorrect password.")
