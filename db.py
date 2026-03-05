# db.py

import sqlite3
from config import DATABASE


def connect():
    return sqlite3.connect(DATABASE)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER,
        subscription TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id, subscription) VALUES (?, ?)",
        (user_id, "none")
    )

    conn.commit()
    conn.close()
