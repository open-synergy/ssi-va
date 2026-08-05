# Edit Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Financial Accounting > Bank & Cash > VA Generators\
> **Actor:** user in group `Virtual Account Generator / User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group `Virtual Account Generator / User`.

## Flow

1. Open the **Financial Accounting > Bank & Cash > VA Generators** menu.
2. Find and open the record to edit.
3. Change the required fields as needed:
   - **Generator Type**, **Bank**, **Biller**, **Merchant**, **Bank Account Usage**:
     only editable while the document is in **Draft** status.
   - Changing **Bank** clears **Biller** and **Merchant**.
   - **Exporter**: editable in **Draft** status, and remains editable even after the
     document reaches **Done** — so an already-**Done** document that was left without
     one can still be fixed without cancelling it.
4. The **Source Data** and **Generated Bank Accounts** tabs cannot be edited from the
   form in any state. **Source Data** is populated only by the Generate VA wizard at
   creation (see `01-create`); **Generated Bank Accounts** is populated automatically
   when the document reaches the **Done** state.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
