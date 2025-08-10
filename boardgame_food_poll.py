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

# --- Page Title
