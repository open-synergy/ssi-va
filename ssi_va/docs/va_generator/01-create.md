# Create Virtual Account Generator

> **Module:** ssi_va\
> **Model:** `va_generator`\
> **Menu:** Contacts\
> **Actor:** user in group `Virtual Account Generator / User`\
> **State:** `—` → `draft`\
> **Requires:** `ssi_va/ir_model/04-add-generate-va-wizard`

A `va_generator` document is never created directly from the **VA Generators** menu —
its **Source Data** tab is readonly in every state, and a document without at least one
source data line is rejected when it is confirmed. The only way to create a
`va_generator` document that can actually be confirmed is the **Generate VA** wizard,
launched from the **Action** menu of the model the Virtual Accounts are generated for
(the "source model"). This IK uses `res.partner` (the **Contacts** menu) as the source
model, since the **Generate VA** wizard binding is registered there by default; the same
flow applies to any other model once its binding has been registered (see
**Pre-Condition**).

## Pre-Condition

- **Config:** A **Generate VA** entry exists in the source model's **Action** menu (see
  `ir_model/04-add-generate-va-wizard`). Already registered by default for
  `res.partner`; any other source model requires that procedure to be run first.
- **Data:** At least one `va_generator_type` record exists.
- **Data:** At least one `va_biller` record exists with a bank code registered for the
  intended bank.
- **Access:** User is in group `Virtual Account Generator / User`.

## Flow

1. Open the **Contacts** menu.
2. Select one or more partner records to generate Virtual Accounts for (check the
   checkbox).
3. Click **Action** > **Generate VA**.
4. In the wizard that appears, fill in the fields:
   - **Generator Type** _(required)_: Select the generator type whose Python code
     computes the unique VA code. A generator type restricted to a different model than
     the one this wizard was launched from is rejected when **Generate VA** is pressed.
   - **Bank** _(required)_: Select the bank the generated Virtual Account numbers are
     for. Changing this field clears **Biller** and **Merchant**.
   - **Biller** _(required)_: Select the biller. Only billers that have a Virtual
     Account code registered for the selected **Bank** are offered.
   - **Merchant**: Optional. Select the merchant registered under the selected biller.
     Only merchants that have a biller code registered for the selected **Biller** are
     offered. Left empty, Virtual Account numbers are generated at biller level.
   - **Bank Account Usage**: Optional. Usage/purpose copied to every generated bank
     account.
   - **Exporter**: Optional. Layout and file format used when generating the export file
     for the resulting document. Can also be set later, directly on the document.
5. Click **Generate VA**.

## Post-Condition

- A new `va_generator` document is created and opened, in **Draft** status.
- The **Source Data** tab is populated with one line per selected source record.
- The document number is still **/** — it is only assigned once the document reaches the
  **Done** state.
