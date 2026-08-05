# Restart Approval Process — Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Financial Accounting > Bank & Cash > VA Generators\
> **Actor:** user in group `Virtual Account Generator / Validator`\
> **Requires:** `04-confirm`

This action reloads the approval template and restarts the approval process from the
beginning, without changing any of the document's own data (biller, bank, merchant,
source data, ...). It exists to recover a document that reached **Waiting for Approval**
without ever getting an approval template resolved (for example, no `approval.template`
matched the document at Confirm time) — in that situation the document has no approver
and the **Approve**/**Reject** buttons never become available to anyone.

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** No approval template is currently resolved for this document (the
  **Approval Template** field is empty). This is what makes the **Restart Approval
  Process** button appear — once a template is resolved and approvers exist, the button
  no longer shows for this document.
- **Config:** An active `policy.template` grants `restart_approval_ok` for state
  `confirm` to the actor's group.
- **Access:** User is in group `Virtual Account Generator / Validator`.

## Flow

1. Open the **Financial Accounting > Bank & Cash > VA Generators** menu.
2. Open the record whose approval process is stuck.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Any existing approval records for the document are removed, and the approval template
  is re-evaluated against the currently configured `approval.template` records.
- If a matching `approval.template` is now found, it is set on the document and fresh
  approval records are created for each of its approver levels, starting the approval
  process from the first level — the same result as a fresh Confirm.
- If still no `approval.template` matches, the document remains in **Waiting for
  Approval** without an approver, and the **Restart Approval Process** button remains
  available.
- Status remains **Waiting for Approval** either way — this action never changes the
  document's `state`.
