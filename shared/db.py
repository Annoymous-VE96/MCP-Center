import sqlite3
from pathlib import Path

# MCP_Center/shared/db.py  ->  parents[1] = MCP_Center/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "mcp_center.db"

# Helper
def get_connection() -> sqlite3.Connection:
    """Opens a connection. Call this fresh each time, don't share across requests."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # access columns by name, e.g. row["title"]
    return conn


def init_db() -> None:
    """Creates tables if they don't exist. Call this once when the server starts."""
    conn = get_connection()
    cursor = conn.cursor()

    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS tasks (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         title TEXT NOT NULL,
    #         description TEXT NOT NULL DEFAULT '',
    #         created_at TEXT NOT NULL DEFAULT (datetime('now'))
    #     )
    # """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


def log_activity(domain: str, action: str, summary: str = "") -> None:
    """Every domain's tools.py calls this after a successful real action."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO logs (domain, action) VALUES (?, ?)",
        (domain, action),
    )
    conn.commit()
    conn.close()