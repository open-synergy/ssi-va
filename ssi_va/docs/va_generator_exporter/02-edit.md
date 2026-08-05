# Edit Virtual Account Generator Exporter

> **Module:** ssi_va\
> **Model:** `va_generator_exporter`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Generator
> Exporters\
> **Actor:** user in group `Virtual Account Generator Exporter`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Record:** The record to edit already exists.
- **Config:** An active `sequence.template` for model `va_generator_exporter` is
  configured. Only needed if the **Generate Code** button will be used to auto-assign
  the **Code** field.
- **Access:** User is in group `Virtual Account Generator Exporter`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Generator
   Exporters** menu.
2. Find and open the record to edit.
3. Click **Generate Code** in the header to assign a value to the **Code** field from
   the configured sequence template — for example after resetting **Code** back to
   **/**. Only applies when **Code** is still **/**; records with a manually entered
   code are left unchanged.
4. On the **Export Configuration** tab, change **Format** and/or **CSV Delimiter** as
   needed. **CSV Delimiter** only applies when **Format** is **CSV** — the field is
   hidden when **Format** is **XLSX**.
5. On the **Python Code** tab, edit the **Python Code** field as needed — for example
   after the export layout changes. It must keep assigning a list to the variable
   `result`, where every item of that list is a list or tuple representing one row. The
   variables available to the code are exactly the ones sent by `va_generator` when the
   export file is generated: `generator`, `biller`, `merchant`, `bank_account_ids`.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- If **Generate Code** was used, the **Code** field now holds a value from the
  configured sequence template.
