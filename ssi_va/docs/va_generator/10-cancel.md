# Cancel Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Financial Accounting > Bank & Cash > VA Generators\
> **Actor:** user in group `Virtual Account Generator / Validator`\
> **State:** `draft` | `confirm` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group `Virtual Account Generator / Validator`.

## Flow

1. Open the **Financial Accounting > Bank & Cash > VA Generators** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the **Select Cancel Reason** wizard, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- Every Virtual Account bank account listed in the **Generated Bank Accounts** tab is
  deleted, so the tab becomes empty. This also applies when the document is cancelled
  from **Done** — any Virtual Account numbers already generated are removed together
  with the change of status, and the document must go through **Confirm**/**Approve**
  again to regenerate them.
- A notification is posted on the document's chatter (e.g. _"Virtual Account Generator
  ... cancelled"_).
