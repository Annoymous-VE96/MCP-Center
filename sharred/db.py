import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent.parent

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Let me access the columns by name
    return conn

def init_db() -> None:
    conn = get_connection()
    