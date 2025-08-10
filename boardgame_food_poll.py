# file: boardgame_food_poll.py
import streamlit as st
from collections import Counter

st.title("🍕 Board Game Night Food Poll 🎲")

# Food options
food_options = [
    "Panda Express",
    "Wing Stop",
    "Marco's Pizza",
    "Ocha Thai",
    "Popeye's"
]

# Store all votes in session state
if "votes" not in st.session_state:
    st.session_state.votes = {}  # key = username, value = food choice

# Ask for user name to track votes
username = st.text_input("Enter your name to vote:")

if username:
    # If the user has already voted, preselect their choice
    current_vote = st.session_state.votes.get(username, food_options[0])
    food_choice = st.radio("Choose one:", food_options, index=food_options.index(current_vote))

    # Update the vote whenever the user clicks submit
    if st.button("Submit / Update Vote"):
        st.session_state.votes[username] = food_choice
        st.success(f"{username}, your vote for {food_choice} has been recorded ✅")

# Show results if any votes exist
if st.session_state.votes:
    st.subheader("Current Results:")
    counts = Counter(st.session_state.votes.values())

    # Display results table
    st.table([[food, count] for food, count in counts.items()])

    # Most popular choice(s)
    max_votes = max(counts.values())
    popular_choices = [food for food, count in counts.items() if count == max_votes]
    st.markdown(f"**🥇 Most Popular:** {', '.join(popular_choices)} ({max_votes} votes)")

else:
    st.info("No votes yet. Be the first to choose!")
