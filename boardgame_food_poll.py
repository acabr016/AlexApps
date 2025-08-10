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

# --- Inject mobile-friendly CSS ---
st.markdown(
    """
    <style>
    /* Make tables horizontally scrollable on small screens */
    .dataframe, table {
        width: 100% !important;
        overflow-x: auto;
        display: block;
    }
    /* Smaller text and inputs on small devices */
    @media (max-width: 600px) {
        .stTextInput > div > input {
            font-size: 14px !important;
            padding: 8px !important;
        }
        .stRadio > div {
            font-size: 14px !important;
        }
        .stButton > button {
            font-size: 14px !important;
            padding: 8px 12px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Page Title ---
st.title("🍕 Board Game Night Food Poll 🎲")
st.subheader("Vote for your favorite food for the game night!")

# --- Voting input inside container ---
with st.container():
    username = st.text_input("Enter your name:")

    if username.strip():
        if username in votes_df["Name"].values:
            current_choice = votes_df.loc[votes_df["Name"] == username, "Choice"].values[0]
        else:
            current_choice = food_options[0]

        food_choice = st.radio("Choose one:", food_options,
