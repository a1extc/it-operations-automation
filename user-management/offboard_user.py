import argparse # accepts the user's email address from the command line.
import json # reads and updates the user database.
import logging # records successful and failed offboarding attempts.

from pathlib import Path # handles file locations.


DATA_FILE = Path(__file__).parent / "users.json"
LOG_FILE = Path(__file__).parent / "offboarding.log"


def load_users():
    """Load existing user records from the JSON database."""

    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def find_user(users, email):
    """Find a user by email address."""

    email = email.strip().lower()

    for user in users:
        if user["email"] == email:
            return user

    return None


def remove_user(users, email):
    """Remove a user from the user database."""

    email = email.strip().lower()

    updated_users = [
        user for user in users
        if user["email"] != email
    ]

    return updated_users

def save_users(users):
    """Save updated user records safely to the JSON database."""

    temp_file = DATA_FILE.with_suffix(".tmp")

    try:
        with open(temp_file, "w") as file:
            json.dump(users, file, indent=4)

        temp_file.replace(DATA_FILE)

    except OSError:
        if temp_file.exists():
            temp_file.unlink()
        raise


def offboard_user(email):
    """Offboard a user by removing their record from the database."""

    users = load_users()

    user = find_user(users, email)

    if user is None:
        logging.warning(
            "Offboarding rejected: user not found (%s)",
            email
        )
        raise ValueError("No user found with this email address.")

    updated_users = remove_user(users, email)

    save_users(updated_users)

    logging.info(
        "Successfully offboarded: %s",
        email.strip().lower()
    )

    return user


def parse_arguments():
    """Parse command-line arguments required to offboard a user."""

    parser = argparse.ArgumentParser(
        description="Offboard an existing user account"
    )

    parser.add_argument(
        "--email",
        required=True,
        help="Email address of the user to offboard"
    )

    return parser.parse_args()


if __name__ == "__main__":

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True
    )

    args = parse_arguments()

    try:
        user = offboard_user(args.email)

        print(
            "Successfully offboarded:",
            user["first_name"],
            user["last_name"],
            "(" + user["email"] + ")"
        )

    except ValueError as error:
        logging.error("Offboarding failed: %s", error)
        print("Offboarding failed:", error)

    except OSError as error:
        logging.error("File operation failed: %s", error)
        print("Offboarding failed due to a file error:", error)