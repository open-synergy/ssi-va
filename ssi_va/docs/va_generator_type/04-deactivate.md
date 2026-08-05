# Deactivate Virtual Account Generator Type

> **Module:** ssi_va\
> **Model:** `va_generator_type`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Generator Types\
> **Actor:** user in group `Virtual Account Generator Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Virtual Account Generator Type`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Generator Types**
   menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated generator types cannot be selected when generating new Virtual Account
  numbers.
- Virtual Account data that already references this generator type can still be viewed.
