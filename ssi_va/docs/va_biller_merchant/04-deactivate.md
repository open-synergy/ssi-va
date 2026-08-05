# Deactivate Virtual Account Biller Merchant

> **Module:** ssi_va\
> **Model:** `va_biller_merchant`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Biller Merchants\
> **Actor:** user in group `Virtual Account Biller Merchant`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Virtual Account Biller Merchant`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Biller
   Merchants** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated biller merchants cannot be selected when generating new Virtual Account
  numbers.
- Virtual Account data that already references this merchant can still be viewed.
