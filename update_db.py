import sqlite3


def init_db():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review TEXT,
            cover TEXT DEFAULT NULL
        )
    """)
    conn.commit()
    conn.close()

conn = sqlite3.connect("books.db")
c = conn.cursor()

# Missing columns add karna (Agar already exist nahi karte)
try:
    c.execute("ALTER TABLE books ADD COLUMN rating INTEGER")
    print("✅ 'rating' column added successfully!")
except sqlite3.OperationalError:
    print("⚠️ 'rating' column already exists.")

try:
    c.execute("ALTER TABLE books ADD COLUMN review TEXT")
    print("✅ 'review' column added successfully!")
except sqlite3.OperationalError:
    print("⚠️ 'review' column already exists.")

conn.commit()
conn.close()

print("✅ Database structure updated successfully!")
