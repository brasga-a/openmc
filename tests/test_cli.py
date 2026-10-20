import unittest
from unittest.mock import patch

from openmc.modules import cli


class CliTests(unittest.TestCase):
    def test_help_does_not_initialize_database(self):
        with patch("sys.argv", ["openmc", "--help"]), \
             patch("openmc.modules.cli.database.init_db") as init_db:
            with self.assertRaises(SystemExit) as exit_context:
                cli.main()
        self.assertEqual(exit_context.exception.code, 0)
        init_db.assert_not_called()
