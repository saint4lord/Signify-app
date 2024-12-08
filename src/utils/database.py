import sqlite3
import bcrypt

# create and setup db
def initialize_db():
    conn = sqlite3.connect("uses.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS userse (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   email TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL
                   )
            ''')
    conn.commit()
    conn.close()

# add users function
def add_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
    except sqlite3.EntegrityError:
        print("Email already exists!")

    conn.close()

# check login function
def validate_login(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    return False

initialize_db()