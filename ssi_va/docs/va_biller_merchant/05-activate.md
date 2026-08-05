# Activate Virtual Account Biller Merchant

> **Module:** ssi_va\
> **Model:** `va_biller_merchant`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Biller Merchants\
> **Actor:** user in group `Virtual Account Biller Merchant`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Virtual Account Biller Merchant`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Biller
   Merchants** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again when generating new Virtual Account numbers.
