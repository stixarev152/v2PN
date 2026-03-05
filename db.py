import sqlite3
import time

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
ref INTEGER,
balance INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subs(
user_id INTEGER,
key TEXT,
expire INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payments(
user_id INTEGER,
amount INTEGER,
status TEXT
)
""")

conn.commit()


def add_user(user_id, ref=None):
    cursor.execute("INSERT OR IGNORE INTO users(id,ref) VALUES(?,?)",(user_id,ref))
    conn.commit()


def add_sub(user_id,key,days):
    expire = int(time.time()) + days*86400
    cursor.execute("INSERT INTO subs VALUES(?,?,?)",(user_id,key,expire))
    conn.commit()


def get_sub(user_id):
    cursor.execute("SELECT key,expire FROM subs WHERE user_id=?",(user_id,))
    return cursor.fetchone()


def delete_sub(user_id):
    cursor.execute("DELETE FROM subs WHERE user_id=?",(user_id,))
    conn.commit()
