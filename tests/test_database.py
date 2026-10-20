import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from openmc.modules import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.path_patch = patch("openmc.modules.database.data_dir", return_value=self.root)
        self.path_patch.start()
        self.addCleanup(self.path_patch.stop)

    def test_register_loader_upserts_without_duplicates(self):
        database.init_db()
        database.register_loader("vanilla", "1.21.4", "release", "old", "/old")
        database.register_loader("vanilla", "1.21.4", "release", "new", "/new")
        records = database.get_loaders()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][1:], ("vanilla", "1.21.4", "release", "new", "/new"))

    def test_init_db_migrates_old_duplicate_records(self):
        conn = sqlite3.connect(self.root / "chest.db")
        conn.execute("""
            CREATE TABLE loaders (
                id INTEGER PRIMARY KEY, name TEXT, version TEXT,
                type TEXT, sha1 TEXT, path TEXT
            )
        """)
        conn.executemany("""
            INSERT INTO loaders (name, version, type, sha1, path)
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("1.16.2", "1.16.2", "release", "old", "/old"),
            ("1.16.2", "1.16.2", "release", "new", "/new"),
        ])
        conn.commit()
        conn.close()

        database.init_db()
        database.init_db()
        records = database.get_loaders()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][1:], ("vanilla", "1.16.2", "release", "new", "/new"))
