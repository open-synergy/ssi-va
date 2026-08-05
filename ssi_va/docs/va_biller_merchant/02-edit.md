# Edit Virtual Account Biller Merchant

> **Module:** ssi_va\
> **Model:** `va_biller_merchant`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Biller Merchants\
> **Actor:** user in group `Virtual Account Biller Merchant`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Record:** The record to edit already exists.
- **Config:** An active `sequence.template` for model `va_biller_merchant` is
  configured. Only needed if the **Generate Code** button will be used to auto-assign
  the **Code** field.
- **Access:** User is in group `Virtual Account Biller Merchant`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Biller
   Merchants** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. Click **Generate Code** in the header to assign a value to the **Code** field from
   the configured sequence template — for example after resetting **Code** back to
   **/**. Only applies when **Code** is still **/**; records with a manually entered
   code are left unchanged.
5. On the **Biller Codes** tab, add, edit, or remove lines to update the
   biller-bank-specific merchant codes for this merchant. Repeat the following steps
   as many times as needed:
   - Click **Add a line** to add a new biller code, or click an existing line to edit
     it.
   - Fill in each line with:
     - **Biller Bank Code** _(required)_: Select the biller-bank code line (a
       `va_biller.code` record, displayed as "Biller - Bank (Code)") that this
       merchant code is registered for. This field selects a **biller-bank
       combination**, not a biller or a bank directly. Each biller-bank code line can
       be used only once per merchant.
     - **Bank**: Automatically filled from the selected **Biller Bank Code** and
       cannot be changed.
     - **Merchant Code** _(required)_: Enter the merchant code registered for the
       selected biller-bank combination, used when generating Virtual Account numbers
       for this merchant.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- If **Generate Code** was used, the **Code** field now holds a value from the
  configured sequence template.
- Biller code lines added, edited, or removed on the **Biller Codes** tab are
  reflected in the corresponding `va_biller_merchant.code` records, with **Bank**
  derived from the selected **Biller Bank Code**.
