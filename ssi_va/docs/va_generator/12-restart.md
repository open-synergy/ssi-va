# Restart Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Financial Accounting > Bank & Cash > VA Generators\
> **Actor:** user in group `Virtual Account Generator / Validator`\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` grants `restart_ok` for that state to the
  actor's group.
- **Access:** User is in group `Virtual Account Generator / Validator`.

## Flow

1. Open the **Financial Accounting > Bank & Cash > VA Generators** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
