# Create Virtual Account Biller Merchant

> **Module:** ssi_va\
> **Model:** `va_biller_merchant`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Biller Merchants\
> **Actor:** user in group `Virtual Account Biller Merchant`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` for model `va_biller_merchant` is
  configured. Only needed if the **Generate Code** button will be used to auto-assign
  the **Code** field.
- **Data:** At least one `va_biller` record exists with at least one line on its **Bank
  Codes** tab (a `va_biller.code` record). Without it, the **Biller Bank Code** field on
  the **Biller Codes** tab offers no options to select.
- **Access:** User is in group `Virtual Account Biller Merchant`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Biller
   Merchants** menu.
2. Click the **Create** button.
3. Fill in the required fields:
   - **Name** _(required)_: Enter a name that identifies this merchant.
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it blank for
     now and assign it later with the **Generate Code** button.
4. Click **Generate Code** in the header to assign a value to the **Code** field from
   the configured sequence template. Only applies when **Code** is still **/** —
   records with a manually entered code are left unchanged. Skip this step if a code
   was already entered manually in step 3.
5. On the **Biller Codes** tab, add lines to record the biller-bank-specific merchant
   codes for this merchant. Repeat the following steps as many times as needed:
   - Click **Add a line**.
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

- A new **Virtual Account Biller Merchant** record is created and appears in the
  Biller Merchants list.
- If **Generate Code** was used, the **Code** field now holds a value from the
  configured sequence template.
- Each line added on the **Biller Codes** tab creates a corresponding
  `va_biller_merchant.code` record linked to this merchant, with **Bank** derived from
  the selected **Biller Bank Code**.
