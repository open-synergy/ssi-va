# Create Virtual Account Generator Exporter

> **Module:** ssi_va\
> **Model:** `va_generator_exporter`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Generator
> Exporters\
> **Actor:** user in group `Virtual Account Generator Exporter`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` for model `va_generator_exporter` is
  configured. Only needed if the **Generate Code** button will be used to
  auto-assign the **Code** field.
- **Access:** User is in group `Virtual Account Generator Exporter`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Generator
   Exporters** menu.
2. Click the **Create** button.
3. Fill in the required fields:
   - **Name** _(required)_: Enter a name that identifies this export layout.
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it blank
     for now and assign it later with the **Generate Code** button.
4. Click **Generate Code** in the header to assign a value to the **Code** field
   from the configured sequence template. Only applies when **Code** is still
   **/** — records with a manually entered code are left unchanged. Skip this
   step if a code was already entered manually in step 3.
5. On the **Export Configuration** tab, fill in:
   - **Format** _(required)_: Select **XLSX** or **CSV**. Default is **XLSX**.
   - **CSV Delimiter**: Only applies when **Format** is **CSV** — the field is
     hidden when **Format** is **XLSX**. Enter the column delimiter character
     used when writing the CSV file (e.g. `,` or `;`).
6. On the **Python Code** tab, review/edit the **Python Code** field
   _(required)_. This code is executed (via `safe_eval`) to compute the rows to
   export, and **must assign a list to the variable `result`, where every item
   of that list is itself a list or tuple representing one row** — the first
   row is usually a header row, but that is a decision made in the code
   snippet, not a system rule. In addition to the standard safe_eval helpers
   (`env`, `document`, `time`, `datetime`, `dateutil`, `timezone`,
   `float_compare`, `b64encode`, `b64decode`), the following variables are
   available exactly as sent by `va_generator` when the export file is
   generated: `generator`, `biller`, `merchant`, `bank_account_ids`. A default
   value (`result = []`) is pre-filled; replace it with the actual row
   computation logic.
7. Click **Save**.

## Post-Condition

- A new **Virtual Account Generator Exporter** record is created and appears in
  the Generator Exporters list.
- If **Generate Code** was used, the **Code** field now holds a value from the
  configured sequence template.
