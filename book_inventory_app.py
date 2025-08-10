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
st.title("📚 Our Library Inventory")

init_db()

menu = st.sidebar.radio("Menu", ["View Inventory", "Admin Login"])

if menu == "View Inventory":
    st.subheader("📋 Book Inventory")

    # Search bar
    search_query = st.text_input("🔍 Search by Title or Author", placeholder="Type to search...")
    books = get_books(search_query)

    if not books:
        st.info("No books found.")
    else:
        for book in books:
            book_id, title, author, status, borrower, borrow_date = book
            st.markdown(f"**{title}** by *{author}*")
            st.write(f"Status: {status}")
            if borrower:
                st.write(f"Borrowed by: {borrower} on {borrow_date}")

            if status == "In Library":
    with st.expander("📤 Lend this book"):
        friend = st.text_input(f"Friend's Name (Book ID {book_id})", key=f"friend_{book_id}")
        borrow_date_input = st.date_input(f"Borrow Date (Book ID {book_id})", key=f"date_{book_id}")

        lend_password = st.text_input(f"Enter password to lend (Book ID {book_id})", type="password", key=f"lendpass_{book_id}")
        if st.button(f"Lend Book {book_id}"):
            if lend_password != ADMIN_PASSWORD:
                st.error("❌ Incorrect password. Cannot lend the book.")
            elif not friend:
                st.warning("Please enter friend's name before lending.")
            else:
                update_status(book_id, f"Borrowed by {friend}", borrower=friend, borrow_date=str(borrow_date_input))
                st.success(f"📤 '{title}' lent to {friend}")

                st.warning("Please enter friend's name before lending.")
            else:
                update_status(book_id, f"Borrowed by {friend}", borrower=friend, borrow_date=str(borrow_date_input))
                st.success(f"📤 '{title}' lent to {friend}")
