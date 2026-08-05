# Reject Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Financial Accounting > Bank & Cash > VA Generators\
> **Actor:** approver in group `Virtual Account Generator / Validator` on the currently pending
> approval level\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `reject_ok` to the actor's group.
- **Access:** User is in group `Virtual Account Generator / Validator`.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**.

## Flow

1. Open the **Financial Accounting > Bank & Cash > VA Generators** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
- A notification is posted on the document's chatter (e.g. _"Virtual Account Generator
  ... rejected"_).
