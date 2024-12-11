import sqlite3
import bcrypt
import os

# Path to the database file in the same directory
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

# Initialize and set up the database
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a new user
def add_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Store as string
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Email already exists!")
    finally:
        conn.close()

# Function to validate login credentials
def validate_login(email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password = result[0]  # Stored hash as string
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))  # Convert back to bytes
    return False

# Initialize the database on first run
initialize_db()
add_user("test", "1234")
