import sqlite3

conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    ai TEXT
)
""")

def save_chat(user, ai):
    cursor.execute("INSERT INTO chats (user, ai) VALUES (?, ?)", (user, ai))
    conn.commit()

def get_chats():
    cursor.execute("SELECT * FROM chats ORDER BY id DESC")
    return cursor.fetchall()