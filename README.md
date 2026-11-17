
# IT Operations Automation: User Management

## Overview

This project demonstrates Python-based IT operations automation through user provisioning and employee offboarding workflows.

The scripts automate common user management tasks, validate account information, prevent duplicate records, and maintain structured logs of operations. User records are stored in a local JSON database.

The project emphasizes reliable automation, error handling, data integrity, automated testing, and operational documentation.

## Features

### 1. User Provisioning
- Create user records using command-line arguments.
- Validate required user information.
- Check for duplicate email addresses.
- Store user records in a JSON database.
- Log successful and failed provisioning attempts.

### 2. User Offboarding
- Locate existing users by email address.
- Remove the specified user record.
- Preserve other user records.
- Handle attempts to offboard nonexistent users.
- Log successful and failed offboarding attempts.

### 3. Reliability and Testing
- Implement error handling for file operations.
- Use temporary files when saving updated user records.
- Preserve existing database contents when save operations fail.
- Implement structured logging to record operational activity and errors.
- Include automated tests using Python's built-in unittest framework.

### 4. Operational Documentation
- User provisioning runbook.
- User offboarding runbook.
- Troubleshooting guide.

## Technologies

- Python
- JSON
- Command-Line Interfaces (CLI)
- Logging
- Unit Testing (unittest)
- Git and GitHub

## Project Structure

```text
it-operations-automation/
│
├── README.md
├── .gitignore
│
├── user-management/
│   ├── provision_user.py
│   ├── offboard_user.py
│   ├── test_save_users.py
│   └── test_offboard_user.py
│
└── docs/
    ├── provisioning_runbook.md
    ├── offboarding_runbook.md
    └── troubleshooting.md
```

## Getting Started

### Prerequisites

- Python 3 installed.
- Git installed.
- A local copy of this repository.

No external Python packages are required.

### Clone the Repository

```bash
git clone <your-github-repository-url>
cd it-operations-automation
```

### Provision a User

Run the following command from the project root:

```bash
python user-management/provision_user.py \
    --first-name Alex \
    --last-name Morgan \
    --email alex.morgan@example.com \
    --department IT
```

### Offboard a User

```bash
python user-management/offboard_user.py \
    --email alex.morgan@example.com
```

## Running Automated Tests

Run the provisioning save tests:

```bash
python -m unittest discover -s user-management -p "test_save_users.py" -v
```

Run the offboarding tests:

```bash
python -m unittest discover -s user-management -p "test_offboard_user.py" -v
```

## Logging

The scripts generate separate log files in the `user-management/` directory:

- `provisioning.log` records provisioning activity.
- `offboarding.log` records offboarding activity.

Logs capture successful operations, warnings, and errors to support troubleshooting and operational visibility.

## Documentation

Additional operational documentation is available in the `docs/` directory:

- [Provisioning Runbook](docs/provisioning_runbook.md)
- [Offboarding Runbook](docs/offboarding_runbook.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

## Local Data and Logs

User records and generated log files are maintained locally and excluded from version control.

- `users.json` stores local user records.
- `provisioning.log` records provisioning activity.
- `offboarding.log` records offboarding activity.

The project uses fictional user information for demonstration purposes.

## Project Scope and Limitations

This project simulates user account lifecycle management using a local JSON database.

It does not currently integrate with:
- Microsoft Entra ID
- Active Directory
- Microsoft 365
- Other enterprise identity providers

The scripts manage local user records and do not disable real organizational accounts or revoke access to external services.

## Future Improvements

Potential extensions include:

- Integration with an identity provider.
- Automated license assignment and reclamation.
- Employee onboarding and offboarding notifications.
- Centralized database storage.
- Additional monitoring and audit capabilities.
