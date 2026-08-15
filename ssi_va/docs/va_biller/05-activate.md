# Activate Virtual Account Biller

> **Module:** ssi_va\
> **Model:** `va_biller`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Billers\
> **Actor:** user in group `Virtual Account Biller`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Virtual Account Biller`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Billers** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again when generating new Virtual Account numbers.
