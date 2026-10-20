import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".local/share/openmc/chest.db"

def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    conn = connect()

    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS loaders (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    version TEXT,
                    type TEXT,
                    sha1 TEXT,
                    path TEXT
                )
            """)
    finally:
        conn.close()

def register_loader( n: str, v: str, t: str, k: str, p: str ) -> None:
    conn = connect()

    try:
        with conn:
            conn.execute(
                """
                INSERT INTO loaders
                    (name, version, type, sha1, path)
                VALUES (?, ?, ?, ?, ?)
                """,
                (n, v, t, k, p)
            )
    finally:
        conn.close()

def get_loaders() -> list[tuple]:
    conn = connect()

    try:
        return conn.execute("SELECT * FROM loaders").fetchall()

    finally:
        conn.close()
