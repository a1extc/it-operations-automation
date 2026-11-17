import argparse # accepts information through the command line.
import json # format used to store structured information.
import logging # records successful and failed provision attempts.

from pathlib import Path # Python module that helps us work with file and folder paths.


# Location of the JSON file containing user records
DATA_FILE = Path(__file__).parent / "users.json"
TEMP_FILE = DATA_FILE.with_suffix(".tmp")


def load_users():
    """Load existing user records from the JSON file."""

    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def validate_user(first_name, last_name, email, department):
    """Check that all required user information is valid."""

    if not first_name.strip():
        raise ValueError("First name is required.")

    if not last_name.strip():
        raise ValueError("Last name is required.")

    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("A valid email address is required.")

    if not department.strip():
        raise ValueError("Department is required.")


def create_user(first_name, last_name, email, department):
    """Validate information and create a user dictionary."""

    validate_user(first_name, last_name, email, department)

    user = {
        "first_name": first_name.strip(),
        "last_name": last_name.strip(),
        "email": email.strip().lower(),
        "department": department.strip()
    }

    return user


def email_exists(users, email):
    """Check whether a user's email already exists."""

    for user in users:
        if user["email"] == email.strip().lower():
            return True

    return False


def save_users(users):
    """Save user records safely to the JSON database."""

    try:
        with open(TEMP_FILE, "w") as file:
            json.dump(users, file, indent=4)

        TEMP_FILE.replace(DATA_FILE)

    except OSError: # remove incomplete temporary file
        if TEMP_FILE.exists():
            TEMP_FILE.unlink()
        raise


def parse_arguments():
    """Parse command-line arguments required to provision a new user."""
    parser = argparse.ArgumentParser(
        description="Provision a new user account"
    )

    parser.add_argument("--first-name", required=True)
    parser.add_argument("--last-name", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--department", required=True)

    return parser.parse_args()


def provision_user(first_name, last_name, email, department):
    """Provision a user in the local JSON database."""

    users = load_users()

    new_user = create_user(
        first_name,
        last_name,
        email,
        department
    )

    if email_exists(users, new_user["email"]):
        logging.warning(
            "Provisioning rejected: duplicate email %s",
            new_user["email"]
        )
        raise ValueError("A user with this email already exists.")

    users.append(new_user)
    save_users(users)

    logging.info(
        "Successfully provisioned: %s",
        new_user["email"]
    )

    return new_user


if __name__ == "__main__":
    logging.basicConfig(
        filename=Path(__file__).parent / "provisioning.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True
    )

    args = parse_arguments()

    try:
        user = provision_user(
            args.first_name,
            args.last_name,
            args.email,
            args.department
        )

        print("Provisioned user:", user)

    except ValueError as error:
        logging.error("Provisioning failed: %s", error)
        print("Provisioning failed:", error)
