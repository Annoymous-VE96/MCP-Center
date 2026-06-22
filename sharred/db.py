import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent.parent

# Opens the database connection 
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE) # returns a connection object
    conn.row_factory = sqlite3.Row # Let me access the columns by name
    return conn

# Creates the tables if not already exists
def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor() # object that sends the SQL commands to db to run + reads the responses

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGAR PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL, 
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL DEFAULT (dateime('now'))
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log(
            id INTEGAR PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL, 
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL DEFAULT (dateime('now'))
        )
    """)

    conn.commit()
    conn.close()
    

# Helper every domain's tools.py calls after a successful action 
def log_activity(domain: str, action: str, summary: str = "") -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO activity_log(domain, action, summary) VALUES (?, ?, ?)", 
        (domain, action, summary)
    )

    conn.commit()
    conn.close()
