# Approve Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Financial Accounting > Bank & Cash > VA Generators\
> **Actor:** approver in group `Virtual Account Generator / Validator` on the currently pending
> approval level\
> **State:** `confirm` → `done`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record.
- **Access:** User is in group `Virtual Account Generator / Validator`.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The standard approval template uses sequential approval, so only the
  first unapproved level is pending.

## Flow

1. Open the **Financial Accounting > Bank & Cash > VA Generators** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels after this approval, status remains
  **Waiting for Approval** and the next level becomes pending.
- If this was the last pending approval level, the document automatically transitions to
  **Done** — there is no separate **Done** button for this model, and this happens even
  if every line in the **Source Data** tab ends up skipped. As part of that automatic
  transition:
  - The document number is issued, replacing **/**.
  - The **Generated Bank Accounts** tab is populated only for combinations of **Source
    Data** line and biller/merchant bank code whose Virtual Account number does not yet
    exist in the system. A combination whose number already exists is skipped instead,
    and the corresponding **Source Data** line's **Generation Status** is **Skipped**.
