# Delete Virtual Account Biller

> **Module:** ssi_va
> **Model:** `va_biller`
> **Menu:** Financial Accounting > Configuration > Virtual Account > Billers
> **Actor:** user in group *Virtual Account Biller*
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is not referenced by any Virtual Account generation data.
- **Access:** User is in group *Virtual Account Biller*.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Billers** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records, together with their **Bank Codes** lines, are permanently
  removed from the system.
