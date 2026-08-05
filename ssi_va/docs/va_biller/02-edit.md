# Edit Virtual Account Biller

> **Module:** ssi_va
> **Model:** `va_biller`
> **Menu:** Financial Accounting > Configuration > Virtual Account > Billers
> **Actor:** user in group *Virtual Account Biller*
> **Requires:** `01-create`
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Record:** The record to edit already exists.
- **Config:** An active `sequence.template` for model `va_biller` is configured. Only
  needed if the **Generate Code** button will be used to auto-assign the **Code** field.
- **Access:** User is in group *Virtual Account Biller*.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Billers** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. Click **Generate Code** in the header to assign a value to the **Code** field from
   the configured sequence template — for example after resetting **Code** back to
   **/**. Only applies when **Code** is still **/**; records with a manually entered code
   are left unchanged.
5. On the **Bank Codes** tab, add, edit, or remove lines to update the bank-specific
   Virtual Account codes for this biller. Repeat the following steps as many times as
   needed:
   - Click **Add a line** to add a new bank code, or click an existing line to edit it.
   - Fill in each line with:
     - **Bank** *(required)*: Select the bank that issued the biller code. Each bank can
       be used only once per biller.
     - **Biller Code** *(required)*: Enter the biller code issued by the bank, used when
       generating Virtual Account numbers for this bank.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- If **Generate Code** was used, the **Code** field now holds a value from the configured
  sequence template.
- Bank code lines added, edited, or removed on the **Bank Codes** tab are reflected in
  the corresponding `va_biller.code` records.
