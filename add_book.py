import sqlite3

conn = sqlite3.connect("books.db")
c = conn.cursor()

# Naya table bina 'cover' column ke banayenge
c.execute("""
    CREATE TABLE books_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        status TEXT CHECK(status IN ('Unread', 'In Progress', 'Read')),
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        review TEXT
    )
""")

# Purane table se data migrate karenge (cover column ko ignore karenge)
c.execute("""
    INSERT INTO books_new (id, title, author, status, rating, review)
    SELECT id, title, author, status, rating, review FROM books
""")

# Purane table ko hata kar naye table ka naam 'books' rakh denge
c.execute("DROP TABLE books")
c.execute("ALTER TABLE books_new RENAME TO books")

conn.commit()
conn.close()

print("✅ 'cover' column successfully removed!")
