# file: boardgame_food_poll.py
import streamlit as st
from collections import Counter

# Title of the app
st.title("🍕 Board Game Night Food Poll 🎲")

# Initialize session state for storing votes
if "votes" not in st.session_state:
    st.session_state.votes = []

st.subheader("Vote for your favorite food for the game night:")

# Input from user
food_choice = st.text_input("Enter your preferred food (e.g., Pizza, Tacos, Sushi):")

if st.button("Submit"):
    if food_choice.strip():
        st.session_state.votes.append(food_choice.strip().title())
        st.success(f"You voted for: {food_choice.strip().title()} ✅")
    else:
        st.warning("Please enter a valid food choice before submitting.")

# Display current vote results
if st.session_state.votes:
    st.subheader("Current Results:")
    counts = Counter(st.session_state.votes)
    
    # Display table of results
    st.table([[food, count] for food, count in counts.items()])
    
    # Show most popular choice(s)
    max_votes = max(counts.values())
    popular_choices = [food for food, count in counts.items() if count == max_votes]
    st.markdown(f"**🥇 Most Popular:** {', '.join(popular_choices)} ({max_votes} votes)")

else:
    st.info("No votes yet. Be the first to choose!")

