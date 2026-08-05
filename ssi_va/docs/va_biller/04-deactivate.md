# Deactivate Virtual Account Biller

> **Module:** ssi_va\
> **Model:** `va_biller`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Billers\
> **Actor:** user in group `Virtual Account Biller`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Virtual Account Biller`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Billers** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated billers cannot be selected when generating new Virtual Account numbers.
- Virtual Account data that already references this biller can still be viewed.
