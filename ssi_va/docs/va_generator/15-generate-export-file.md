# Generate Export File — Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Financial Accounting > Bank & Cash > VA Generators\
> **Actor:** user in group `Virtual Account Generator / User`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Done**.
- **Record:** The **Exporter** field is filled in. It remains editable while the
  document is in **Done** status, so a document that already reached **Done** without an
  Exporter set can still be fixed here directly — there is no need to cancel it first
  (cancelling would delete every generated Virtual Account, see `10-cancel`).
- **Access:** User is in group `Virtual Account Generator / User`.

## Flow

1. Open the **Financial Accounting > Bank & Cash > VA Generators** menu.
2. Open the record to generate the export file for.
3. If **Exporter** is not yet set, select one now.
4. Click the **Generate Export File** button (`action_generate_export_file`).

## Post-Condition

- A new attachment is added to the document, named from the document number, a creation
  timestamp, and a file extension matching the selected Exporter's format (e.g.
  `VA.00001-20260805_143000.xlsx`). The content of the generated file is not covered by
  this IK.

Either of the two checks in **Pre-Condition** that is not met blocks the action with a
corresponding error message instead of producing the result above:

- Document not in **Done** status: _"Document is not in the done state"_.
- No **Exporter** selected: _"No exporter has been selected"_.
