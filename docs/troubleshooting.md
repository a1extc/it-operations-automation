
# IT Operations Automation - Troubleshooting Guide

## 1. Purpose

This guide documents common issues encountered when using the user provisioning and offboarding automation scripts.

It provides possible causes and recommended troubleshooting steps.

## 2. Provisioning Issues

| Error | Possible Cause | Resolution |
|---|---|---|
| A user with this email already exists | Duplicate email address | Check the user database before retrying |
| A valid email address is required | Incorrect email format | Verify the email address |
| First name is required | Missing first name | Provide a first name |
| Last name is required | Missing last name | Provide a last name |
| Department is required | Missing department | Provide a department |

## 3. Offboarding Issues

| Error | Possible Cause | Resolution |
|---|---|---|
| No user found with this email address | Email does not match an existing record | Verify the email address |
| File operation failed | Database cannot be updated | Check file permissions and available disk space |

## 4. Database Issues

The project uses a local JSON file to store user records:

`user-management/users.json`

If unexpected behavior occurs:

1. Check whether the file exists.
2. Open the file and verify that its contents are valid JSON.
3. Confirm that user records contain the expected fields.
4. Check that the project has permission to read and write the file.
5. Avoid manually editing the file while a script is running.

## 5. Log Review

The scripts maintain separate log files:

- `user-management/provisioning.log`
- `user-management/offboarding.log`

Log severity levels:

| Level | Meaning |
|---|---|
| INFO | Successful operations |
| WARNING | Unexpected conditions, such as duplicate accounts or missing users |
| ERROR | Failed operations |

Review the relevant log file to identify when an operation occurred and why it failed.

## 6. Testing and Validation

Automated tests are available to verify core functionality.

Run provisioning tests:

```bash
python -m unittest discover -s user-management -p "test_provision_user.py" -v
```

Run offboarding tests:

```bash
python -m unittest discover -s user-management -p "test_offboard_user.py" -v
```

Tests use temporary data so they do not modify the actual user database.

## 7. Operational Best Practices

- Verify user information before making account changes.
- Review existing records before provisioning or offboarding.
- Check logs after failed operations.
- Keep backups of important user data.
- Use fictional information when demonstrating this portfolio project.
- Test code changes before using the automation.

## 8. Project Limitations

This project demonstrates local user-record management using Python and JSON.

It does not currently:
- Create or disable actual Microsoft 365 or Entra ID accounts.
- Revoke application access or active sessions.
- Remove licenses from external services.
- Integrate with an enterprise identity provider.
