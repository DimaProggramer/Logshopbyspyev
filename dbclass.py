from imports import *

conn = sqlite3.connect('users.db')
c = conn.cursor()

def init_db():
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance INTEGER, accept BOOLEAN DEFAULT 0)")
    conn.commit()

def user_exists(user_id):
    c.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    return bool(c.fetchone())
    
def add_user(user_id):
    if not user_exists(user_id):
        c.execute("INSERT INTO users (user_id, balance) VALUES (?, 0)", (user_id,))
        conn.commit()
    
def get_balance(user_id):
    c.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    return c.fetchone()[0]
    
def update_balance(user_id, amount_rub):
    c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount_rub, user_id))
    conn.commit()

def get_total_users():
    c.execute("SELECT COUNT(*) FROM users")
    return c.fetchone()[0]

def get_all_users():
    c.execute("SELECT user_id FROM users")
    users = [{"id": row[0]} for row in c.fetchall()]
    return users
