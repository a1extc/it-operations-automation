
# User Offboarding Runbook

## 1. Purpose

This runbook explains how to offboard an existing user using the Python user management automation script.

The script locates a user by email address, removes the matching record from the local JSON database, and logs the operation.

## 2. Prerequisites

Before running the script, ensure that:

- Python 3 is installed.
- The project repository is available locally.
- You are running commands from the project root directory.
- The `user-management` directory contains [offboard_user.py](../user-management/offboard_user.py).
- The user account exists in the local JSON database.

## 3. Required Information

Collect and verify the following information:

| Field | Description |
|---|---|
| Email | Email address associated with the account |

Verify the email address before proceeding to avoid removing the wrong account.

## 4. Offboarding Procedure

Run the following command from the project root directory:

```bash
python user-management/offboard_user.py \
    --email alex.morgan@example.com
```

Replace the example email address with the account being offboarded.

## 5. Expected Results

### Successful Offboarding

Expected output:

```text
Successfully offboarded: Alex Morgan (alex.morgan@example.com)
```

The user's record is removed from:

`user-management/users.json`

Other user records remain unchanged.

### User Not Found

If no account matches the supplied email address, the operation is rejected.

Expected output:

```text
Offboarding failed: No user found with this email address.
```

The existing user database remains unchanged.

## 6. Logging

Offboarding activity is recorded in:

`user-management/offboarding.log`

The log includes:

- Successful offboarding operations (INFO).
- Attempts to offboard nonexistent users (WARNING).
- Failed offboarding operations (ERROR).

## 7. Troubleshooting

| Issue | Possible Cause | Resolution |
|---|---|---|
| User not found | Email does not match an existing account | Verify the email address |
| File operation error | Database cannot be updated | Check file permissions and available disk space |
| Invalid command | Required email argument was omitted | Supply the `--email` argument |
| Unexpected database contents | Incorrect or outdated user records | Review the JSON database before retrying |

## 8. Important Notes

- Verify the user's identity and email address before offboarding.
- Do not use real employee information in this portfolio demonstration.
- Confirm that the correct record was removed.
- Review the offboarding log after each operation.
- This project removes records from a local JSON database; it does not disable real organizational accounts or revoke access to external services.
