
import unittest
import tempfile
import json

from pathlib import Path
from unittest.mock import patch, mock_open

import offboard_user


class TestOffboarding(unittest.TestCase):

    def setUp(self):
        """Create sample users and a temporary database for each test."""

        self.users = [
            {
                "first_name": "Alex",
                "last_name": "Morgan",
                "email": "alex.morgan@example.com",
                "department": "IT"
            },
            {
                "first_name": "Jordan",
                "last_name": "Lee",
                "email": "jordan.lee@example.com",
                "department": "Finance"
            }
        ]

        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "users.json"

        with open(self.data_file, "w") as file:
            json.dump(self.users, file, indent=4)

        self.data_file_patch = patch.object(
            offboard_user, "DATA_FILE", self.data_file
        )
        self.data_file_patch.start()

    def tearDown(self):
        """Restore patched settings and remove temporary files."""

        self.data_file_patch.stop()
        self.temp_dir.cleanup()

    def test_find_existing_user(self):
        user = offboard_user.find_user(
            self.users, "alex.morgan@example.com"
        )

        self.assertIsNotNone(user)
        self.assertEqual(user["first_name"], "Alex")

    def test_find_nonexistent_user(self):
        user = offboard_user.find_user(
            self.users, "nobody@example.com"
        )

        self.assertIsNone(user)

    def test_remove_user(self):
        updated_users = offboard_user.remove_user(
            self.users, "alex.morgan@example.com"
        )

        self.assertEqual(len(updated_users), 1)
        self.assertEqual(
            updated_users[0]["email"],
            "jordan.lee@example.com"
        )

    def test_remove_user_preserves_original_list(self):
        original_count = len(self.users)

        offboard_user.remove_user(
            self.users, "alex.morgan@example.com"
        )

        self.assertEqual(len(self.users), original_count)

    def test_successful_offboarding(self):
        user = offboard_user.offboard_user(
            "alex.morgan@example.com"
        )

        self.assertEqual(user["first_name"], "Alex")

        with open(self.data_file, "r") as file:
            saved_users = json.load(file)

        self.assertEqual(len(saved_users), 1)
        self.assertEqual(
            saved_users[0]["email"],
            "jordan.lee@example.com"
        )

    def test_offboarding_nonexistent_user(self):
        with self.assertRaises(ValueError):
            offboard_user.offboard_user("nobody@example.com")

        with open(self.data_file, "r") as file:
            saved_users = json.load(file)

        self.assertEqual(len(saved_users), 2)


    def test_save_users_failure_preserves_original_file(self):
        original_content = self.data_file.read_text()

        with patch(
            "builtins.open",
            mock_open()
        ) as mocked_file:

            mocked_file.side_effect = OSError("Disk write failed")

            with self.assertRaises(OSError):
                offboard_user.save_users([])

        self.assertEqual(
            self.data_file.read_text(),
            original_content
        )

        self.assertFalse(
            self.data_file.with_suffix(".tmp").exists()
        )


if __name__ == "__main__":
    unittest.main()
