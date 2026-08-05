# Reset Document Number — Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Financial Accounting > Bank & Cash > VA Generators\
> **Actor:** user in group `Virtual Account Generator / Validator`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` grants `manual_number_ok` for state `draft` to
  the actor's group. Without it, the **Reset Document Number** button does not appear.
- **Access:** User is in group `Virtual Account Generator / Validator`.

## Flow

1. Open the **Financial Accounting > Bank & Cash > VA Generators** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number once it reaches the **Done** state,
  according to the sequence template configuration.
