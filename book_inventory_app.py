# book_inventory_app.py

import streamlit as st
import sqlite3
from datetime import datetime
from PIL import Image
import easyocr
import io
import os

# ------------------------------
# Database setup
# ------------------------------
DB_FILE = "books.db"

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
    c.execute("SELECT * FROM books")
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

# ------------------------------
# OCR from image
# ------------------------------
def extract_text_from_image(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    detected_text = " ".join([res[1] for res in result])
    return detected_text

# ------------------------------
# Streamlit App
# ------------------------------
st.set_page_config(page_title="📚 My Book Inventory", layout="centered")
st.title("📚 My Book Inventory")

init_db()

menu = st.sidebar.radio("Menu", ["Add Book", "View Inventory"])

if menu == "Add Book":
    st.subheader("➕ Add a Book")
    option = st.radio("Choose input method:", ["Manual Entry", "Scan Book Cover"])

    title = ""
    author = ""

    if option == "Manual Entry":
        title = st.text_input("Book Title")
        author = st.text_input("Author")

    elif option == "Scan Book Cover":
        uploaded_file = st.file_uploader("Upload a photo of the book cover", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Book Cover", use_column_width=True)

            # Save to temporary file for OCR
            temp_image_path = "temp_book_cover.jpg"
            image.save(temp_image_path)

            with st.spinner("Reading text from cover..."):
                detected_text = extract_text_from_image(temp_image_path)
                st.write("**Detected Text:**", detected_text)

            # Let user edit extracted data
            title = st.text_input("Book Title", detected_text)
            author = st.text_input("Author")

    if st.button("Add to Inventory"):
        if title and author:
            add_book(title, author)
            st.success(f"✅ '{title}' by {author} added to inventory!")
        else:
            st.warning("Please enter both Title and Author.")

elif menu == "View Inventory":
    st.subheader("📋 Book Inventory")
    books = get_books()

    if not books:
        st.info("No books in inventory yet.")
    else:
        for book in books:
            book_id, title, author, status, borrower, borrow_date = book
            st.markdown(f"**{title}** by *{author}*")
            st.write(f"Status: {status}")
            if status != "In Library":
                st.write(f"Borrowed by: {borrower} on {borrow_date}")

            if status == "In Library":
                with st.expander("📤 Lend this book"):
                    friend = st.text_input(f"Friend's Name (Book ID {book_id})", key=f"friend_{book_id}")
                    if st.button(f"Lend Book {book_id}"):
                        if friend:
                            update_status(book_id, f"Borrowed by {friend}", borrower=friend, borrow_date=datetime.now().strftime("%Y-%m-%d"))
                            st.success(f"📤 '{title}' lent to {friend}")
                        else:
                            st.warning("Enter friend's name before lending.")
            else:
                if st.button(f"📥 Mark as Returned (Book ID {book_id})"):
                    update_status(book_id, "In Library", borrower=None, borrow_date=None)
                    st.success(f"📥 '{title}' marked as returned.")

            st.write("---")
