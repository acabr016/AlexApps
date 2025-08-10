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

def get_books():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM books ORDER BY title ASC")
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
    st.subheader("📋 Book Inventory")
    books = get_books()

    if not books:
        st.info("No books in inventory yet.")
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
                    if st.button(f"Lend Book {book_id}"):
                        if friend:
                            update_status(book_id, f"Borrowed by {friend}", borrower=friend, borrow_date=str(borrow_date_input))
                            st.success(f"📤 '{title}' lent to {friend}")
                        else:
                            st.warning("Enter friend's name before lending.")
            else:
                if st.button(f"📥 Mark as Returned (Book ID {book_id})"):
                    update_status(book_id, "In Library", borrower=None, borrow_date=None)
                    st.success(f"📥 '{title}' marked as returned.")

            st.write("---")

elif menu == "Admin Login":
    password = st.text_input("Enter admin password:", type="password")
    if password == ADMIN_PASSWORD:
        st.success("✅ Logged in as admin")
        st.subheader("➕ Add a Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        if st.button("Add to Inventory"):
            if title and author:
                add_book(title, author)
                st.success(f"✅ '{title}' by {author} added to inventory!")
            else:
                st.warning("Please enter both Title and Author.")

        st.subheader("🗑 Delete a Book")
        books = get_books()
        if books:
            book_to_delete = st.selectbox("Select a book to delete:", [(b[0], f"{b[1]} by {b[2]}") for b in books], format_func=lambda x: x[1])
            if st.button("Delete Book"):
                delete_book(book_to_delete[0])
                st.success("Book deleted successfully!")
