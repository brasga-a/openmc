import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from openmc.modules import request


class FakeResponse:
    def __init__(self, *, data=None, chunks=None):
        self.data = data
        self.chunks = chunks or []
        self.headers = {}

    def raise_for_status(self):
        pass

    def json(self):
        return self.data

    def iter_content(self, chunk_size):
        yield from self.chunks

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


class RequestTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        path_patch = patch("openmc.modules.request.data_dir", return_value=self.root)
        path_patch.start()
        self.addCleanup(path_patch.stop)

    def responses(self, content=b"valid server data", bad_hash=False):
        actual_sha1 = hashlib.sha1(content).hexdigest()
        return [
            FakeResponse(data={"versions": [
                {"id": "1.21.4", "url": "https://example.test/version", "type": "release"}
            ]}),
            FakeResponse(data={"downloads": {"server": {
                "url": "https://example.test/server", "sha1": "0" * 40 if bad_hash else actual_sha1,
                "size": len(content),
            }}}),
            FakeResponse(chunks=[content[:3], content[3:]]),
        ]

    def test_valid_jar_is_installed_and_registered(self):
        data = b"valid server data"
        with patch("openmc.modules.request.requests.get", side_effect=self.responses(data)), \
             patch("openmc.modules.request.database.register_loader") as register:
            request.add_loader("1.21.4")
        jar = self.root / "loaders/1.21.4.jar"
        self.assertEqual(jar.read_bytes(), data)
        self.assertFalse((self.root / "loaders/1.21.4.jar.part").exists())
        register.assert_called_once_with("vanilla", "1.21.4", "release", hashlib.sha1(data).hexdigest(), str(jar))

    def test_hash_mismatch_deletes_partial_and_does_not_register(self):
        with patch("openmc.modules.request.requests.get", side_effect=self.responses(b"bad", bad_hash=True)), \
             patch("openmc.modules.request.database.register_loader") as register:
            with self.assertRaisesRegex(ValueError, "SHA-1 mismatch"):
                request.add_loader("1.21.4")
        self.assertFalse((self.root / "loaders/1.21.4.jar.part").exists())
        self.assertFalse((self.root / "loaders/1.21.4.jar").exists())
        register.assert_not_called()

    def test_version_without_server_jar(self):
        response = self.responses()[0]
        with patch("openmc.modules.request.requests.get", side_effect=[response, FakeResponse(data={"downloads": {}})]):
            with self.assertRaisesRegex(ValueError, "no server JAR"):
                request.add_loader("1.21.4")

    def test_unknown_version(self):
        with patch("openmc.modules.request.requests.get", return_value=self.responses()[0]):
            with self.assertRaisesRegex(ValueError, "not found"):
                request.add_loader("nonexistent")
