# Create Virtual Account Biller

> **Module:** ssi_va\
> **Model:** `va_biller`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Billers\
> **Actor:** user in group `Virtual Account Biller`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` for model `va_biller` is configured. Only
  needed if the **Generate Code** button will be used to auto-assign the **Code** field.
- **Data:** At least one `res.bank` record exists. Only needed if bank-specific codes
  will be added on the **Bank Codes** tab.
- **Access:** User is in group `Virtual Account Biller`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Billers** menu.
2. Click the **Create** button.
3. Fill in the required fields:
   - **Name** _(required)_: Enter a name that identifies this biller.
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it blank for
     now and assign it later with the **Generate Code** button.
4. Click **Generate Code** in the header to assign a value to the **Code** field from
   the configured sequence template. Only applies when **Code** is still **/** — records
   with a manually entered code are left unchanged. Skip this step if a code was already
   entered manually in step 3.
5. On the **Bank Codes** tab, add lines to record the bank-specific Virtual Account
   codes for this biller. Repeat the following steps as many times as needed:
   - Click **Add a line**.
   - Fill in each line with:
     - **Bank** _(required)_: Select the bank that issued the biller code. Each bank can
       be used only once per biller.
     - **Biller Code** _(required)_: Enter the biller code issued by the bank, used when
       generating Virtual Account numbers for this bank.
6. Click **Save**.

## Post-Condition

- A new **Virtual Account Biller** record is created and appears in the Billers list.
- If **Generate Code** was used, the **Code** field now holds a value from the
  configured sequence template.
- Each line added on the **Bank Codes** tab creates a corresponding `va_biller.code`
  record linked to this biller.
