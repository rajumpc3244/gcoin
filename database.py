import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, username TEXT, points INTEGER DEFAULT 0, ref_by INTEGER)""")
    conn.commit()
    conn.close()

def add_user(user_id, username, ref_by=None):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO users (id, username, ref_by) VALUES (?, ?, ?)", (user_id, username, ref_by))
        if ref_by:
            c.execute("UPDATE users SET points = points + 10 WHERE id=?", (ref_by,))
    conn.commit()
    conn.close()

def get_points(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def add_points(user_id, amount):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET points = points + ? WHERE id=?", (amount, user_id))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        username TEXT, 
        points INTEGER DEFAULT 0, 
        ref_by INTEGER,
        last_claim INTEGER DEFAULT 0
    )""")
    conn.commit()
    conn.close()

import time

def can_claim_daily(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT last_claim FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    now = int(time.time())
    if result and now - result[0] >= 86400:  # 86400 = 24 hours
        return True
    return False

def update_claim_time(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET last_claim = ? WHERE id=?", (int(time.time()), user_id))
    conn.commit()
    conn.close()
