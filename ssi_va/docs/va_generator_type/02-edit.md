# Edit Virtual Account Generator Type

> **Module:** ssi_va\
> **Model:** `va_generator_type`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Generator Types\
> **Actor:** user in group `Virtual Account Generator Type`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Record:** The record to edit already exists.
- **Config:** An active `sequence.template` for model `va_generator_type` is configured.
  Only needed if the **Generate Code** button will be used to auto-assign the **Code**
  field.
- **Access:** User is in group `Virtual Account Generator Type`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Generator Types**
   menu.
2. Find and open the record to edit.
3. Change the required fields, including the **Restrict to Model** field if the
   generator type's applicable model needs to change.
4. Click **Generate Code** in the header to assign a value to the **Code** field from
   the configured sequence template — for example after resetting **Code** back to
   **/**. Only applies when **Code** is still **/**; records with a manually entered
   code are left unchanged.
5. On the **Python Code** tab, edit the **Python Code** field as needed — for example
   after the unique-code composition rule changes. It must keep assigning a string to
   the variable `result`.
6. On the **Partner Resolution Python Code** tab, edit the **Partner Resolution Python
   Code** field as needed — for example after the source data no longer maps directly to
   a partner. It must keep assigning exactly one `res.partner` record to the variable
   `result`.
7. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- If **Generate Code** was used, the **Code** field now holds a value from the
  configured sequence template.
