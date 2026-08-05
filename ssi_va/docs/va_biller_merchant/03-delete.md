# Delete Virtual Account Biller Merchant

> **Module:** ssi_va\
> **Model:** `va_biller_merchant`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Biller Merchants\
> **Actor:** user in group `Virtual Account Biller Merchant`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is not referenced by any Virtual Account generation data.
- **Access:** User is in group `Virtual Account Biller Merchant`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Biller
   Merchants** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records, together with their **Biller Codes** lines, are permanently
  removed from the system.
