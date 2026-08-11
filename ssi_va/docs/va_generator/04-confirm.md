# Confirm Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Financial Accounting > Bank & Cash > VA Generators\
> **Actor:** user in group `Virtual Account Generator / User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** At least one line exists in the **Source Data** tab.
- **Data:** The selected **Biller** has a Virtual Account code registered for the
  selected **Bank**.
- **Data:** If **Merchant** is set, it has a biller code registered for the combination
  of the selected **Biller** and **Bank**.
- **Data:** Every line in the **Source Data** tab can be resolved into exactly one
  `res.partner` record by the selected **Generator Type**'s partner resolution code.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record.
- **Access:** User is in group `Virtual Account Generator / User`.

## Flow

1. Open the **Financial Accounting > Bank & Cash > VA Generators** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the matching approval
  template.
- Every line in the **Source Data** tab receives a **Generation Status** of either **To
  Generate** or **Skipped**. A **Skipped** line shows the **VA Number** that is already
  taken, along with the **Existing Bank Accounts** that caused it to be skipped.

Any of the four checks in **Pre-Condition** that is not met blocks the Confirm action
with a corresponding error message instead of producing the result above:

- No source data line: _"No source data has been added"_.
- Biller without a code for the selected bank: _"Biller ... has no Virtual Account code
  registered for bank ..."_.
- Merchant without a biller code for the selected biller: _"Merchant ... has no biller
  code registered for biller ..."_.
- A source data line that cannot be resolved into a `res.partner` record: _"Source data
  ... could not be resolved into a res.partner record: ..."_.
