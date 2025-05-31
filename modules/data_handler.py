import sqlite3

def setup_database():
    conn = sqlite3.connect("data/productivity.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL,
        app TEXT,
        title TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_activity(activity):
    conn = sqlite3.connect("data/productivity.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO activities (timestamp, app, title) VALUES (?, ?, ?)",
                   (activity["timestamp"], activity["app"], activity["title"]))
    conn.commit()
    conn.close()