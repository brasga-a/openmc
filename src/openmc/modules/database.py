"""SQLite persistence for installed server loaders."""

import sqlite3

from openmc.modules.paths import data_dir


def connect() -> sqlite3.Connection:
    db_path = data_dir() / "chest.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def init_db() -> None:
    conn = connect()
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS loaders (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    type TEXT NOT NULL,
                    sha1 TEXT NOT NULL,
                    path TEXT NOT NULL
                )
            """)
            # Migrate records written by early OpenMC versions. In those
            # versions, the Minecraft version was also stored as the name.
            conn.execute("""
                UPDATE loaders SET name = 'vanilla'
                WHERE name = version AND type IN ('release', 'snapshot')
            """)
            # Retain the newest record for each loader/version before adding
            # a uniqueness constraint to databases created by older versions.
            conn.execute("""
                DELETE FROM loaders WHERE id NOT IN (
                    SELECT MAX(id) FROM loaders GROUP BY name, version
                )
            """)
            conn.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS loaders_name_version_idx
                ON loaders (name, version)
            """)
    finally:
        conn.close()


def register_loader(n: str, v: str, t: str, k: str, p: str) -> None:
    conn = connect()
    try:
        with conn:
            conn.execute("""
                INSERT INTO loaders (name, version, type, sha1, path)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(name, version) DO UPDATE SET
                    type = excluded.type,
                    sha1 = excluded.sha1,
                    path = excluded.path
            """, (n, v, t, k, p))
    finally:
        conn.close()


def get_loaders() -> list[tuple]:
    conn = connect()
    try:
        return conn.execute("""
            SELECT id, name, version, type, sha1, path
            FROM loaders ORDER BY name, version
        """).fetchall()
    finally:
        conn.close()
