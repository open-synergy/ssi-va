# Activate Virtual Account Generator Type

> **Module:** ssi_va\
> **Model:** `va_generator_type`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Generator Types\
> **Actor:** user in group `Virtual Account Generator Type`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Virtual Account Generator Type`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Generator Types**
   menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again when generating new Virtual Account numbers.
