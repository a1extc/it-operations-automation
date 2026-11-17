import json # lets us read and write JSON data in the test.
import tempfile # helps us create a separate temporary folder for testing.
import unittest # Python's built-in testing framework.
from pathlib import Path # lets us work with file paths.
from unittest.mock import patch # lets us temporarily replace part of the program's behavior so we can simulate a failure.

from provision_user import save_users


class TestSaveUsers(unittest.TestCase):

    def setUp(self):
        # Create a separate temporary folder for testing
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

        self.data_file = self.test_path / "users.json"
        self.temp_file = self.test_path / "users.tmp"

        # Create an original user record
        self.original_users = [
            {
                "first_name": "Alex",
                "last_name": "Morgan",
                "email": "alex.morgan@example.com",
                "department": "Engineering"
            }
        ]

        with open(self.data_file, "w") as file:
            json.dump(self.original_users, file, indent=4)

    def tearDown(self):
        # Remove the temporary test folder after each test
        self.test_dir.cleanup()

    def test_successful_save(self):
        updated_users = self.original_users + [
            {
                "first_name": "Taylor",
                "last_name": "Smith",
                "email": "taylor.smith@example.com",
                "department": "Finance"
            }
        ]

        # Temporarily point the save function to our test files
        with patch("provision_user.DATA_FILE", self.data_file), \
             patch("provision_user.TEMP_FILE", self.temp_file):

            save_users(updated_users)

        with open(self.data_file, "r") as file:
            saved_users = json.load(file)

        self.assertEqual(saved_users, updated_users)
        self.assertFalse(self.temp_file.exists())

    def test_failed_save_preserves_original(self):
        # Simulate a failure while writing the temporary file
        with patch("provision_user.DATA_FILE", self.data_file), \
             patch("provision_user.TEMP_FILE", self.temp_file), \
             patch("provision_user.json.dump", side_effect=OSError("Simulated save failure")):

            with self.assertRaises(OSError):
                save_users([])

        # Confirm the original file was not changed
        with open(self.data_file, "r") as file:
            saved_users = json.load(file)

        self.assertEqual(saved_users, self.original_users)


if __name__ == "__main__":
    unittest.main()
