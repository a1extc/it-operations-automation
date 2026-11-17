
# User Provisioning Runbook

## 1. Purpose

This runbook explains how to provision a new user account using the Python user provisioning automation script.

The script validates user information, checks for duplicate email addresses, creates a user record, and saves the record to a local JSON database.

## 2. Prerequisites

Before running the script, ensure that:

- Python 3 is installed.
- The project repository is available locally.
- You are running commands from the project root directory.
- The `user-management` directory contains [provision_user.py](../user-management/provision_user.py).

## 3. Required Information

Collect the following information before provisioning a user:

| Field | Description |
|---|---|
| First name | User's first name |
| Last name | User's last name |
| Email | Unique user email address |
| Department | User's assigned department |

## 4. Provisioning Procedure

Run the following command from the project root directory:

```bash
python user-management/provision_user.py \
    --first-name Alex \
    --last-name Morgan \
    --email alex.morgan@example.com \
    --department IT
```

Replace the example values with the new user's information.

## 5. Expected Results

### Successful Provisioning

Expected output:

```text
Provisioned user: {'first_name': 'Alex', 'last_name': 'Morgan', 'email': 'alex.morgan@example.com', 'department': 'IT'}
```

The new user record is saved in:

`user-management/users.json`

### Duplicate Email Address

If an account already exists with the supplied email address, provisioning is rejected.

Expected output:

```text
Provisioning failed: A user with this email already exists.
```

### Invalid User Information

The script rejects missing names, invalid email addresses, and missing departments.

Expected output for an invalid email:

```text
Provisioning failed: A valid email address is required.
```

## 6. Logging

Provisioning activity is recorded in:

`user-management/provisioning.log`

The log includes:

- Successful provisioning operations (INFO).
- Duplicate account attempts (WARNING).
- Failed provisioning attempts (ERROR).

## 7. Troubleshooting

| Issue | Possible Cause | Resolution |
|---|---|---|
| Duplicate email | Account already exists | Verify the existing account before retrying |
| Invalid email | Incorrect email format | Check the email address |
| Missing required field | Required information was omitted | Supply all required arguments |
| File operation error | Database cannot be written | Check file permissions and available disk space |
| Python command not found | Python is not installed or not on PATH | Install Python 3 or correct the PATH configuration |

## 8. Important Notes

- Verify user information before provisioning.
- Do not use real employee information in this portfolio demonstration.
- Confirm that the user record was saved successfully.
- Review the provisioning log if an operation fails.
