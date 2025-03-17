import streamlit as st
import sqlite3
import os

# Ensure covers directory exists
if not os.path.exists("covers"):
    os.makedirs("covers")

# Set page configuration
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# --- UI Styling ---
st.markdown("""
    <style>
    .big-font { font-size:22px !important; font-weight: bold; }
    .book-card { border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .stButton > button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Database ---
def init_db():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT CHECK(status IN ('Unread', 'In Progress', 'Read')),
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            review TEXT,
            cover TEXT DEFAULT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Sidebar Navigation ---
st.sidebar.title("📖 Navigation")
selected_page = st.sidebar.radio("📌 Select a Page", ["Home", "Add Book", "Statistics"])

# --- Fetch Books from Database ---
def get_books(status_filter=None):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    query = "SELECT * FROM books"
    params = ()

    if status_filter and status_filter != "All":
        query += " WHERE status = ?"
        params = (status_filter,)

    c.execute(query, params)
    books = c.fetchall()
    conn.close()
    return books

# --- Home Page ---
if selected_page == "Home":
    st.title("📚 Your Personal Library ")
    
    status_filter = st.sidebar.selectbox("Filter by Status", ["All", "Unread", "In Progress", "Read"])
    books = get_books(status_filter if status_filter != "All" else None)

    if books:
        for book in books:
            book_id, title, author, status, rating, review, *cover = book  # Handle extra column
            cover = cover[0] if cover else None  # Ensure cover doesn't cause unpacking errors
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if cover and os.path.exists(cover):
                    st.image(cover, width=100)
                else:
                    st.image("https://via.placeholder.com/100", width=100)  # Default Image
            with col2:
                st.markdown(f"<p class='big-font'>{title} by {author}</p>", unsafe_allow_html=True)
                st.write(f"📖 **Status:** {status}")
                st.write(f"⭐ **Rating:** {rating}/5")
                st.write(f"💬 **Review:** {review}")
                st.markdown("---")
    else:
        st.info("No books available. Add books from the 'Add Book' section.")

# --- Add Book Page ---
elif selected_page == "Add Book":
    st.title("➕ Add a New Book")

    with st.form("add_book_form"):
        title = st.text_input("📖 Book Title")
        author = st.text_input("✍️ Author")
        status = st.selectbox("📂 Status", ["Unread", "In Progress", "Read"])
        rating = st.slider("⭐ Rating", 1, 5, 3)
        review = st.text_area("💬 Review")
        cover_image = st.file_uploader("📷 Upload Book Cover", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("📚 Add Book")
        if submitted:
            if title and author:
                cover_path = None
                if cover_image:
                    cover_path = f"covers/{title.replace(' ', '_')}.jpg"
                    with open(cover_path, "wb") as f:
                        f.write(cover_image.getbuffer())

                conn = sqlite3.connect("books.db")
                c = conn.cursor()
                c.execute("INSERT INTO books (title, author, status, rating, review, cover) VALUES (?, ?, ?, ?, ?, ?)", 
                          (title, author, status, rating, review, cover_path))
                conn.commit()
                conn.close()

                st.success("✅ Book added successfully!")
                st.rerun()

# --- Statistics Page ---
elif selected_page == "Statistics":
    st.title("📊 Reading Statistics")
    books = get_books()
    total_books = len(books)
    completed_books = sum(1 for book in books if book[3] == "Read")
    in_progress_books = sum(1 for book in books if book[3] == "In Progress")
    unread_books = sum(1 for book in books if book[3] == "Unread")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Total Books", total_books)
    col2.metric("✔️ Completed", completed_books)
    col3.metric("📖 In Progress", in_progress_books)
    col4.metric("❌ Unread", unread_books)

    st.markdown("### 📈 Progress Overview")
    progress_percentage = (completed_books / total_books) * 100 if total_books > 0 else 0
    st.progress(progress_percentage / 100)
