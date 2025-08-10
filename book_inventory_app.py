# library_inventory_app.py

import streamlit as st
import sqlite3
from datetime import datetime

DB_FILE = "book_inventory.db"
ADMIN_PASSWORD = "TheLibrary"

# ------------------------------
# Database setup
# ------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    status TEXT DEFAULT 'In Library',
                    borrower TEXT,
                    borrow_date TEXT
                )''')
    conn.commit()
    conn.close()

def add_book(title, author):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

def get_books(search_query=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if search_query:
        search_query = f"%{search_query}%"
        c.execute("""
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ?
            ORDER BY title COLLATE NOCASE ASC
        """, (search_query, search_query))
    else:
        c.execute("SELECT * FROM books ORDER BY title COLLATE NOCASE ASC")
    rows = c.fetchall()
    conn.close()
    return rows

def update_status(book_id, status, borrower=None, borrow_date=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE books SET status=?, borrower=?, borrow_date=? WHERE id=?",
              (status, borrower, borrow_date, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="📚 My Book Inventory", layout="centered")
st.title("📚 My Book Inventory")

init_db()

menu = st.sidebar.radio("Menu", ["View Inventory", "Admin Login"])

if menu == "View Inventory":
    # your code for viewing inventory

elif menu == "Admin Login":
    # your code for admin login

