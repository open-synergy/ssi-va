# Deactivate Virtual Account Generator Exporter

> **Module:** ssi_va\
> **Model:** `va_generator_exporter`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Generator
> Exporters\
> **Actor:** user in group `Virtual Account Generator Exporter`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Virtual Account Generator Exporter`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Generator
   Exporters** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated export layouts cannot be selected as the exporter of a Virtual Account
  generation document.
- Virtual Account data that already references this export layout can still be viewed.
