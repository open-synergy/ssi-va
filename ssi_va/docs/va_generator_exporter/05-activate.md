# Activate Virtual Account Generator Exporter

> **Module:** ssi_va\
> **Model:** `va_generator_exporter`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Generator
> Exporters\
> **Actor:** user in group `Virtual Account Generator Exporter`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Virtual Account Generator Exporter`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Generator
   Exporters** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again as the exporter of a Virtual Account generation
  document.
